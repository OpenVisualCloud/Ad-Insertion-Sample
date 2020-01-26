#!/usr/bin/python3

from os.path import isfile
from subprocess import call
from os import mkdir
from zkstate import ZKState
from abr_hls_dash import GetABRCommand
from messaging import Consumer
import traceback
import time

kafka_topic="content_provider_sched"
kafka_group="content_provider_dash_hls_creator"

archive_root="/var/www/archive"
dash_root="/var/www/video/dash"
hls_root="/var/www/video/hls"

def process_stream(stream):
    stream_name=stream.split("/")[1]
    if not isfile(archive_root+"/"+stream_name): return

    zk=ZKState("/content_provider_transcoder/"+archive_root+"/"+stream)
    if zk.processed(): 
        zk.close()
        return

    if stream.endswith(".mpd"):
        try:
            mkdir(dash_root+"/"+stream_name)
        except:
            pass

        if zk.process_start():
            try:
                cmd = GetABRCommand(archive_root+"/"+stream_name,dash_root+"/"+stream_name,"dash")
                r=call(cmd)
                if r: raise Exception("status code: "+str(r))
                zk.process_end()
            except:
                print(traceback.format_exc(), flush=True)
                zk.process_abort()

    if stream.endswith(".m3u8"):
        try:
            mkdir(hls_root+"/"+stream_name)
        except:
            pass

        if zk.process_start():
            try:
                cmd = GetABRCommand(archive_root+"/"+stream_name,hls_root+"/"+stream_name,"hls")
                r=call(cmd)
                if r: raise Exception("status code: "+str(r))
                zk.process_end()
            except:
                print(traceback.format_exc(), flush=True)
                zk.process_abort()
    zk.close()

c=Consumer(kafka_group)
while True:
    try:
        for message in c.messages(kafka_topic):
            process_stream(message)
    except:
        print(traceback.format_exc(), flush=True)
        time.sleep(2)
c.close()
