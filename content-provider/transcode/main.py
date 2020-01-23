#!/usr/bin/python3

from os.path import isfile
from subprocess import call
from os import mkdir
from zkstate import ZKState
from abr_hls_dash import GetABRCommand
from messaging import Consumer
import time

kafka_topic="content_provider_sched"
kafka_group="content_provider_dash_hls_creator"

archive_root="/var/www/archive"
dash_root="/var/www/video/dash"
hls_root="/var/www/video/hls"

def process_stream(zk, stream):
   stream_name=stream.split("/")[1]
   if not isfile(archive_root+"/"+stream_name): return

   zk.set_path("/content_provider_transcoder/"+archive_root+"/"+stream)
   if zk.processed(): return

   if stream.endswith(".mpd"):
       try:
           mkdir(dash_root+"/"+stream_name)
       except Exception as e:
           print(str(e))

       if zk.process_start():
           try:
               cmd = GetABRCommand(archive_root+"/"+stream_name,dash_root+"/"+stream_name,"dash")
               r=call(cmd)
               if r: raise Exception("status code: "+str(r))
               zk.process_end()
           except Exception as e:
               print(str(e))
               zk.process_abort()
   if stream.endswith(".m3u8"):
       try:
           mkdir(hls_root+"/"+stream_name)
       except Exception as e:
           print(str(e))

       if zk.process_start():
           try:
               cmd = GetABRCommand(archive_root+"/"+stream_name,hls_root+"/"+stream_name,"hls")
               r=call(cmd)
               if r: raise Exception("status code: "+str(r))
               zk.process_end()
           except Exception as e:
               print(str(e))
               zk.process_abort()

if __name__ == "__main__":
    c=Consumer(kafka_group)
    zk=ZKState()
    while True:
        try:
            for message in c.messages(kafka_topic):
                process_stream(zk, message)
        except Exception as e:
            print(str(e))
        time.sleep(2)
    c.close()
    zk.close()
