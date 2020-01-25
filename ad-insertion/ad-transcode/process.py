#!/usr/bin/python3

from os.path import isfile, isdir
from os import mkdir, makedirs, listdir, remove
from abr_hls_dash import GetABRCommand
import multiprocessing
import errno
import time
import json
import subprocess
import requests
import shutil
import traceback

adinsert_archive_root="/var/www/adinsert"
segment_dash_root=adinsert_archive_root+"/segment/dash"
segment_hls_root=adinsert_archive_root+"/segment/hls"
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
    #ad_uri = ad_content_server+"/" +"GibfM0FYj_g.mp4"
    target=adinsert_archive_root+"/" + ad_uri.split("/")[-1]
    #print(target)
    if ad_uri.find("http://") != -1:
        try:
            r = requests.get(ad_uri,timeout=timeout)
            if r.status_code == 200:
                with open(target, "wb") as f:
                    f.write(r.content)
                return target 
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("Error sending status request in ADPrefetch()" + str(e), flush=True)
    elif not isfile(ad_uri):
        print("The ad content uri %s is not a file!"+ad_uri)
        return None 

def ADClipDecision(msg, db):
    duration = msg.time_range[1]-msg.time_range[0]
    query_times = 10
    for t in range(query_times):
        print("query db with time range: "+str(msg.time_range[0])+"-"+str(msg.time_range[1]))
        metaData = db.query(msg.content, msg.time_range, msg.time_field)
        if metaData or msg.bench_mode:
            try:
                jdata = json.dumps({
                    "metadata":metaData,
                    "user":{
                        "name":msg.user_name,
                        "keywords":msg.user_keywords
                    },
                    "bench_mode":msg.bench_mode
                })
                r = requests.post(ad_decision_server, data=jdata, timeout=timeout)
                if r.status_code == 200:
                    ad_info = r.json()
                    print(ad_info,flush=True)
                    return ad_info[0]["source"]["uri"]
            except requests.exceptions.RequestException as e:
                print("Error in ADClipDecision() " + str(e), flush=True)
            return None
        time.sleep(1)
        if t == query_times - 2:
            msg.time_range[0]=msg.time_range[0]-duration/2
    return None

class KafkaMsgParser(object):
    def __init__(self, kafkamsg):
        self.msg = json.loads(kafkamsg)
        self.streaming_type = self.msg["ad_config"]["streaming_type"]

        self.target = self.msg["destination"]["adpath"]
        self.target_path = self.target[0:self.target.rfind("/")]
        self.target_name = self.target.split("/")[-1]

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
        self.bench_mode = self.msg["bench_mode"]
        self.segment_path = segment_hls_root
        if self.streaming_type=="dash":
            self.segment_path = segment_dash_root

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

def ADTranscode(zks, zkd, kafkamsg, db):
    msg=KafkaMsgParser(kafkamsg)
    zks.set_path(msg.target_path, msg.target_name)
    if zks.processed():
        print("AD transcoding finish the clip :",msg.target, flush=True)
        return

    if zks.process_start():
        try:
            makedirs(msg.target_path)
        except Exception as e:
            print("Exception: "+str(e), flush=True)

        stream = ADClipDecision(msg,db)
        if not stream:
            print("Query AD clip failed and fall back to skipped ad clip!", flush=True)
            zks.process_abort()
            return

        try:
            stream_folder = msg.segment_path + "/" + stream.split("/")[-1]
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
            zkd_path="/".join(msg.target.replace(adinsert_archive_root+"/","").split("/")[:-1])
            zkd.set(zk_segment_prefix+"/"+zkd_path+"/link","/adinsert/"+zkd_path)
            print("set "+zk_segment_prefix+"/"+zkd_path+"/link to /adinsert/"+zkd_path, flush=True)
            zks.process_end()
        except Exception as e:
            print(traceback.format_exc(), flush=True)
            zks.process_abort()
