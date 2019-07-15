#!/usr/bin/python3

from os.path import isfile, isdir
from os import mkdir, makedirs, listdir, remove
import errno
import time
from zkstate import ZKState
import json
import threading
import subprocess
import multiprocessing
import requests
from db import DataBase
from abr_hls_dash import GetABRCommand
import shutil

adinsert_archive_root="/var/www/adinsert"
dash_root="/var/www/adinsert/dash"
hls_root="/var/www/adinsert/hls"
fallback_root="/var/www/skipped"

ad_decision_server="http://ad-decision:8080/metadata"
ad_content_server="http://ad-content:8080"

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
 
    def GetRedition(self):
        redition = ([self.width, self.height, self.bitrate, 128000],)
        return redition

# this will
def CopyAD(msg,height,height_list=[2160, 1440, 1080, 720, 480, 360]):
    source_path = msg.target_path
    target_path = msg.target_path
    streaming_type = msg.streaming_type

    all_files = list(listdir(source_path))
    #all_files = list(listdir(target_path))
    org_files = []
    suffix=str(height)+"p"

    #print(all_files)
    for name in all_files:
        if name.startswith(suffix):
            org_files += [name]
    for name in org_files:
        src = source_path + "/" + name
        if streaming_type=="dash" and (name.endswith(".m4s") or name.endswith(".mpd")):
            for item in height_list:
                tmp = name
                dst = target_path + "/" + tmp.replace(str(height),str(item))
                if item != height:
                    shutil.copyfile(src,dst)
        if streaming_type=="hls" and (name.endswith(".ts") or name.endswith(".m3u8")):
            for item in height_list:
                tmp = name
                dst = target_path + "/" + tmp.replace(str(height),str(item))
                if item != height:
                    shutil.copyfile(src,dst)

def CopyADStatic(msg, prefix="na"):
    # first copy all streams
    all_files=list(listdir(fallback_root))
    for name in all_files:
        target_file=msg.target_path+"/"+name
        if msg.streaming_type=="dash" and (name.endswith(".m4s") or name.endswith(".mpd")):
            if not isfile(target_file) or name.startswith(prefix):
                shutil.copyfile(fallback_root+"/"+name,target_file)
        if msg.streaming_type=="hls" and (name.endswith(".ts") or name.endswith(".m3u8")):
            if not isfile(target_file) or name.startswith(prefix):
                shutil.copyfile(fallback_root+"/"+name,target_file)

    # then signal complete for all streams.
    for name in all_files:
        target_file=msg.target_path+"/"+name
        complete_file=msg.target_path+"/"+name+".complete"
        if msg.streaming_type=="dash" and name.endswith(".mpd"):
            if not isfile(complete_file) or name.startswith(prefix):
                SignalCompletion(target_file)
        if msg.streaming_type=="hls" and name.endswith(".m3u8"):
            if not isfile(complete_file) or name.startswith(prefix):
                SignalCompletion(target_file)
    
def SignalCompletion(name):
    with open(name+".complete","w") as f:
        pass

def SignalIncompletion(name):
    try:
        remove(name+".complete")
    except:
        pass

def ADTranscode(kafkamsg,db):
    zk = None

    msg=KafkaMsgParser(kafkamsg)
    # add zk state for each resolution file if we generate the ad clip each time for one solution
    zk=ZKState(msg.target_path, msg.target_name)

    if zk.processed():
        print("AD transcoding finish the clip :",msg.target, flush=True)
        zk.close()
        return


    if zk.process_start():
        try:
            print("mkdir -p "+msg.target_path, flush=True)
            makedirs(msg.target_path)
        except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
            if exc.errno == errno.EEXIST and isdir(msg.target_path):
                pass
            else: raise

        # copy static ADs to fill all resolutions
        CopyADStatic(msg)

        stream = ADClipDecision(msg,db)
        if not stream:
            print("Query AD clip failed and fall back to skipped ad clip!", flush=True)
            # mark zk as incomplete (so that the valid one can be generated next time)
            zk.process_abort()
            zk.close()
            return

        # try to re-generate resolution specific AD
        SignalIncompletion(msg.target)

        try:
            # only generate one resolution for ad segment, if not generated, ad will fall back to skipped ad.
            cmd = GetABRCommand(stream, msg.target_path, msg.streaming_type, msg.GetRedition(), duration=msg.segment_duration, fade_type="audio", content_type="ad")
            process_id = subprocess.Popen(cmd,stdout=subprocess.PIPE)
            # the `multiprocessing.Process` process will wait until
            # the call to the `subprocess.Popen` object is completed
            process_id.wait()
            SignalCompletion(msg.target)
            zk.process_end()
        except Exception as e:
            print(str(e))
            CopyADStatic(msg)
            zk.process_abort()
    zk.close()

class Process(object):
    """This class spawns a subprocess asynchronously and calls a
    `callback` upon completion; it is not meant to be instantiated
    directly (derived classes are called instead)"""

    def __init__(self, type):
        self.db = DataBase()

    def __call__(self, kafkamsg):
    # store the arguments for later retrieval
        self._kafkamsg = kafkamsg
    # define the target function to be called by
    # `multiprocessing.Process`
        def target():

            ADTranscode(self._kafkamsg,self.db)
            # upon completion, call `callback`
            return self.callback()
        mp_process = multiprocessing.Process(target=target)
        # this call issues the call to `target`, but returns immediately
        mp_process.start()
        return mp_process

    def callback(self):
        print("finished ad transcoding command ")
