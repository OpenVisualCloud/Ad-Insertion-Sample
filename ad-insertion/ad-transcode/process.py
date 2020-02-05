#!/usr/bin/python3

from os.path import isfile, isdir
from os import mkdir, makedirs, listdir, remove
from abr_hls_dash import GetABRCommand
from zkdata import ZKData
from zkstate import ZKState
import multiprocessing
import errno
import time
import json
import subprocess
import requests
import shutil
import traceback

adinsert_archive_root="/var/www/adinsert"
adsegment_archive_root="/var/www/adsegment"
dash_root=adinsert_archive_root+"/dash"
hls_root=adinsert_archive_root+"/hls"
zk_segment_prefix="/ad-insertion-segment"

ad_decision_server="http://ad-decision-service:8080/metadata"
ad_content_server="http://ad-content-service:8080"

timeout = 30

request_template={
            "meta-db" : {
                "stream" : "",
                "time_range" : [],
                "time_field" : "time"
             },
            "ad_config": {
                "codec": "AVC",
                "resolution": {
                    "width": 1280,
                    "height": 720,
                },
                "bandwidth": 10000,
                "streaming_type": "hls"
            },
            "destination": {
                "adpath": "/var/www/adinsert/hls/xxx",
            },
            "user_info": {
                "name": "guest",
                "keyword": ["sport","car"]
            },
            "audio_fade": {
                "fade_in": "http://content-provider:8080/hls/7QDJL9c9qTI.mp4/360p_024.ts",
                "fade_out": "http://content-provider:8080/hls/7QDJL9c9qTI.mp4/360p_025.ts",
                "target_path": "/var/www/adinsert/hls/xxx"
            }
        }

def ADPrefetch(ad_uri):
    # retrive the ad from the ad content and save to local adinsert_archive_root firstly and return the local stream name
    target=adinsert_archive_root+"/" + ad_uri.split("/")[-1]
    if ad_uri.find("http://") != -1:
        try:
            print("Retrieve "+ad_uri, flush=True)
            r = requests.get(ad_uri,timeout=timeout)
            if r.status_code == 200:
                with open(target, "wb") as f:
                    f.write(r.content)
                return target 
        except:
            print(traceback.format_exc(), flush=True)
    return None 

def ADClipDecision(msg, db):
    duration = msg.time_range[1]-msg.time_range[0]
    print("query db with time range: "+str(msg.time_range[0])+"-"+str(msg.time_range[1]))
    metaData = db.query(msg.content, msg.time_range, msg.time_field)
    try:
        r=requests.post(ad_decision_server, timeout=timeout, data=json.dumps({
            "metadata":metaData,
            "user":{
                "name":msg.user_name,
                "keywords":msg.user_keywords
            },
        }))
        r.raise_for_status()
        ad_info = r.json()
        return ad_info[0]["source"]["uri"]
    except:
        print(traceback.format_exc(), flush=True)
        return None

class KafkaMsgParser(object):
    def __init__(self, kafkamsg):
        self.msg = json.loads(kafkamsg)
        self.streaming_type = self.msg["ad_config"]["streaming_type"]

        self.target = self.msg["destination"]["adpath"]
        self.target_path = self.target[0:self.target.rfind("/")]
        self.target_name = self.target.split("/")[-1]
        self.start_time = self.msg["start_time"]

        # use mp4 stream name as the index
        self.content = self.msg["meta-db"]["stream"]
        self.time_range = self.msg["meta-db"]["time_range"]
        self.time_field = self.msg["meta-db"]["time_field"]
        self.user_name = self.msg["user_info"]["name"]
        self.user_keywords = self.msg["user_info"]["keywords"]
        self.segment_duration=self.msg["ad_config"]["segment"]
        self.height = self.msg["ad_config"]["resolution"]["height"]
        self.width = self.msg["ad_config"]["resolution"]["width"]
        self.bitrate = self.msg["ad_config"]["bandwidth"]
        self.segment_path = adsegment_archive_root+"/"+self.streaming_type

    def GetRedition(self):
        redition = ([self.width, self.height, self.bitrate, 128000],)
        return redition

def CopyADSegment(msg, stream, prefix="na"):
    segment_folder = msg.segment_path + "/" +  stream.split("/")[-1]
    # first copy all streams
    all_files=list(listdir(segment_folder))
    for name in all_files:
        target_file=msg.target_path+"/"+name
        if msg.streaming_type=="dash" and (name.endswith(".m4s") or name.endswith(".mpd")):
            shutil.copyfile(segment_folder+"/"+name,target_file)
        if msg.streaming_type=="hls" and (name.endswith(".ts") or name.endswith(".m3u8")):
            shutil.copyfile(segment_folder+"/"+name,target_file)

def set_ad_path(path, value):
    zkd=ZKData()
    zkd.set(path, value)
    print("set "+path+" to "+value, flush=True)
    zkd.close()

def ADTranscode(kafkamsg, db):
    msg=KafkaMsgParser(kafkamsg)
    # path: /var/www/adinsert/hls/Content_seq7u10.mp4/adstream/u10/4, name: 360p.m3u8
    zk_path="/ad-transcode/"+ ("/".join(msg.target_path.split("/")[-5:]))
    print("zk_path: "+zk_path+"/"+msg.target_name, flush=True)

    zks=ZKState(zk_path, msg.target_name)
    start_time=time.time()
    if zks.processed():
        print("AD transcoding finish the clip :",msg.target, flush=True)
        zks.close()
        return

    if zks.process_start():
        try:
            makedirs(msg.target_path)
        except:
            pass

        stream = ADClipDecision(msg,db)
        zkd_path="/".join(msg.target.replace(adinsert_archive_root+"/","").split("/")[:-1])
        if not stream:
            set_ad_path(zk_segment_prefix+"/"+zkd_path+"/link","/adstatic")
            zks.process_abort()
        else:
            try:
                stream_folder = msg.segment_path + "/" + stream.split("/")[-1]
                print("Checking pre-transcoded stream: "+stream_folder, flush=True)
                if isdir(stream_folder): # pre-transcoded AD exists
                    print("Prefetch the AD segment {} \n".format(stream_folder),flush=True)
                    CopyADSegment(msg,stream)
                else:
                    print("Transcoding the AD segment {} \n".format(stream),flush=True)
                    # only generate one resolution for ad segment, if not generated, ad will fall back to skipped ad.
                    cmd = GetABRCommand(stream, msg.target_path, msg.streaming_type, msg.GetRedition(), duration=msg.segment_duration, fade_type="audio", content_type="ad")
                    process_id = subprocess.Popen(cmd,stdout=subprocess.PIPE)
                    # the `multiprocessing.Process` process will wait until
                    # the call to the `subprocess.Popen` object is completed
                    process_id.wait()

                # signal that we are ready
                set_ad_path(zk_segment_prefix+"/"+zkd_path+"/link","/adinsert/"+zkd_path)
                zks.process_end()
                print("Status transcode: Timing {0} {1} {2} {3} {4}".format(msg.start_time, start_time, time.time()-start_time, msg.user_name, msg.target), flush=True)
            except Exception as e:
                print(traceback.format_exc(), flush=True)
                set_ad_path(zk_segment_prefix+"/"+zkd_path+"/link","/adstatic")
                zks.process_abort()
    zks.close()
