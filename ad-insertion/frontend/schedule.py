#!/usr/bin/python3

from messaging import Producer
import json
import os
import time

analytics_topic = "seg_analytics_sched"
transcode_topic = "ad_transcode_sched"

class Schedule(object):
    def __init__(self):
        super(Schedule, self).__init__()
        self._producer=Producer()

    def analyze(self, user, seg_info, pipeline):
        request={
            "source": {
                "uri": ""
            },
            "pipeline": pipeline,
            "tags":{
                "seg_time": 0.0
            },
            "parameters": {
                "every-nth-frame":int(os.environ.get("EVERY_NTH_FRAME"))
            },
            "user_info": {
                "name": user,
                "keywords": [] #"keywords": ["sports","animal"]
            },
            "start_time": 0.0
        }
        for item in seg_info["analytics"]:
            temp=request.copy()
            temp["source"]["uri"]=item["stream"]
            temp["tags"]["seg_time"]=item["seg_time"]
            temp["start_time"]=time.time()
            #print("Schedule analysis: "+temp["source"]["uri"], flush=True)
            print("Schedule analysis: Timing {0} {1} {2}".format(temp["start_time"], user, temp["source"]["uri"]), flush=True)
            if "initSeg" in seg_info:
                temp["source"]["uri-init"]=seg_info["initSeg"]
            self._producer.send(analytics_topic, json.dumps(temp))

    def transcode(self, user, seg_info, search_interval=10):
        request={
            "meta-db": {
                "stream": seg_info["stream"],
                "time_range": [
                    0.0,
                    10.0,
                ],
                "time_field": "time",
            },
            "ad_config": {
                "codec": seg_info["codec"],
                "resolution": seg_info["resolution"],
                "bandwidth": seg_info["bandwidth"],
                "streaming_type": seg_info["streaming_type"],
                "duration": seg_info["ad_duration"],
                "segment": seg_info["ad_segment"],
            },
            "destination": {
                "adpath": "",
            },
            "user_info": {
                "name": user,
                "keywords": [] #"keywords": ["sports","animal"]
            },
            "start_time": 0.0
        }
        for item in seg_info["transcode"]:
            temp=request.copy()
            temp["meta-db"]["time_range"]=[item["seg_time"]-search_interval,item["seg_time"]]
            temp["destination"]["adpath"]=item["stream"]
            temp["start_time"]=time.time()
            #print("Schedule transcode: "+temp["destination"]["adpath"], flush=True)
            print("Schedule transcode: Timing {0} {1} {2}".format(temp["start_time"], user, temp["destination"]["adpath"]), flush=True)
            self._producer.send(transcode_topic, json.dumps(temp))

    def flush(self):
        self._producer.flush()
