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
import traceback


video_analytics_topic = "seg_analytics_sched"
machine_prefix = os.environ.get("VA_PRE")
if machine_prefix == None:
    machine_prefix = "VA-"
va = RunVA()

global_total_fps = 0
global_seg_count = 0


def process_stream(streamstring):
    streamjson = ast.literal_eval(streamstring)
    pipeline1 = streamjson["pipeline"] + "/1"
    stream = streamjson['source']['uri']
    user = streamjson["user_info"]["name"]
    elapsed_time = time.time() - streamjson["start_time"]
    print("VA feeder: stream: " + stream + " " + user +
          " elapsed-time on kafka queue:" + str(elapsed_time), flush=True)

    zk_path = None
    init_stream = None
    if 'uri-init' in streamjson['source']:
        init_stream = streamjson['source']['uri-init']

    m1 = re.search(r'(dash/.*)/chunk-stream[0-9]*-([0-9]*.m4s)$', stream)
    if m1:
        zk_path = "/analytics/" + \
            m1.group(1) + "/" + m1.group(2) + "/" + streamjson["pipeline"]

    m1 = re.search("(hls/.*)/[0-9]*p_([0-9]*.ts)$", stream)
    if m1:
        zk_path = "/analytics/" + \
            m1.group(1) + "/" + m1.group(2) + "/" + streamjson["pipeline"]
    print("zk path: " + zk_path, flush=True)

    zk = ZKState(zk_path)
    if zk.processed():
        print("VA feeder: " + user + " " + stream +
              " already complete", flush=True)
        zk.close()
        return

    if zk.process_start():
        merged_segment = None
        if init_stream:
            merged_segment = merge.create_merged_segment(init_stream, stream)
            if merged_segment:
                stream = "file://" + merged_segment
                print("VA feeder: video-analytics merged segment: " +
                      stream, flush=True)

        fps = va.loop({
            "source": {
                "uri": stream,
                "type": "uri"
            },
            "destination": {
                "type": "kafka",
                "host": socket.gethostbyname("kafka-service") + ":9092",
                "topic": "seg_analytics_data"
            },
            "tags": streamjson["tags"],
            "parameters": streamjson["parameters"],
            "user": user,
            "start_time": streamjson["start_time"],
        }, streamjson["pipeline"])

        if fps < 0:
            zk.process_abort()
        else:
            zk.process_end()

        if fps > 0:
            global global_total_fps, global_seg_count
            global_total_fps = global_total_fps + fps
            global_seg_count = global_seg_count + 1
            avg_fps = global_total_fps / global_seg_count
            print("VA statistics : " + "avg_fps " + str(avg_fps) + " " +
                  str(global_total_fps) + " " + str(global_seg_count), flush=True)

        if merged_segment:
            merge.delete_merged_segment(merged_segment)
    zk.close()

if __name__ == "__main__":
    c = Consumer("analytics")
    while True:
        try:
            print("VA feeder: listening to messages", flush=True)
            for msg in c.messages(video_analytics_topic):
                print("VA feeder: recieved message: " + str(msg), flush=True)
                try:
                    process_stream(msg)
                except Exception as e:
                    print("VA feeder: " + str(e), flush=True)
                    traceback.print_exc()
        except Exception as e:
            print("VA feeder: error in main" + str(e), flush=True)
            time.sleep(1)
    c.close()
