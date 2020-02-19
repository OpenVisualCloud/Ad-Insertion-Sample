#!/usr/bin/python3

from messaging import Consumer
from runva import RunVA
import ast
from zkstate import ZKState
import merged_segment as merge
import datetime
import json
import socket
import time
import os
import re
import resource
import gc
import subprocess

video_analytics_topic = "seg_analytics_sched"
machine_prefix=os.environ.get("VA_PRE")
if machine_prefix == None:
    machine_prefix="VA-"
va=RunVA()

def process_stream(streamstring):
    streamjson = ast.literal_eval(streamstring)
    pipeline1 = streamjson["pipeline"]+"/1"
    stream = streamjson['source']['uri']
    print("VA feeder: stream: "+stream, flush=True)
    init_stream = None
    zk_path = None
    if 'uri-init' in streamjson['source']:
        init_stream = streamjson['source']['uri-init']
        print("VA feeder: init_stream: "+init_stream, flush=True)
        zk_path = stream+"/"+pipeline1

    m1 = re.search("(.*)/.*_([0-9]+.ts)$", stream)
    if m1:
        segment = stream.split('/')[-1].split('_')[-1]
        zk_path = m1.group(1)+"/"+segment+"/"+pipeline1

    print("VA feeder: zk_path "+zk_path, flush=True)
    zk=ZKState(zk_path)
    if zk.processed():
        print("VA feeder: " + stream + " already complete", flush=True)
        zk.close()
        return 0

    if zk.process_start():
        merged_segment = None
        if init_stream:
            merged_segment = merge.create_merged_segment(init_stream, stream)
            if merged_segment:
                stream = "file://" + merged_segment
                print("VA feeder: video-analytics merged segment: " +
                      stream, flush=True)
        
        fps=va.loop({
            "source": {
                "uri": stream,
                "type":"uri"
            },
            "destination": {
                "type": "kafka",
                "host": socket.gethostbyname("kafka-service")+":9092",
                "topic": "seg_analytics_data"
            },
            "tags": streamjson["tags"],
            "parameters": streamjson["parameters"],
        }, streamjson["pipeline"])

        if fps<0:
            zk.process_abort()
        else:
            zk.process_end()
            
        if merged_segment:
            merge.delete_merged_segment(merged_segment)
    zk.close()
    return 1

def free_command():
    free = subprocess.check_output(["free","-h","-w"]).decode().split('\n')
    headers = free[0].split()
    memory = free[1].split()
    return dict(zip(headers,memory[1:]))


if __name__ == "__main__":
    c = Consumer("analytics")
    count = 0
    mem = 0
    start = time.time()
    elapsed = 0
    max_time = 60 * 60 * 2
    max_mem = 800
    while True:
        try:
            print("VA feeder: listening to messages", flush=True)
            for msg in c.messages(video_analytics_topic):
                print("VA feeder: recieved message: " + str(msg), flush=True)
                try:
                    count = count + process_stream(msg)
                    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
                    memory_usage = {'count':count,'memory_usage':mem}
                    memory_usage.update(free_command())
                    print(json.dumps(memory_usage))
                    elapsed = time.time() - start
                    if (elapsed>max_time) or (mem>=max_mem):
                        break
                except Exception as e:
                    print("VA feeder: "+str(e), flush=True)
            if (elapsed>max_time) or (mem>=max_mem):
                break
        except Exception as e:
            print("VA feeder: error in main" + str(e), flush=True)
            time.sleep(1)
    if (mem>=max_mem):
        print("Reached Max Memory",flush=True)
    elif (elapsed>max_time):
        print("Reached Max Time",flush=True)
    else:
        print("Exited for unknown reason",flush=True)
    
    #c.close()
