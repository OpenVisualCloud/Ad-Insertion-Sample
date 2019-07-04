#!/usr/bin/python3

from messaging import Producer
import json

analytics_topic = "seg_analytics_sched"
transcode_topic = "ad_transcode_sched"

class Schedule(object):
    def __init__(self):
        super(Schedule, self).__init__()
        self._producer=Producer()

    def analyze(self, seg_info, pipeline):
        request={
            "source": {
                "uri": ""
            },
            "pipeline": pipeline,
            "tags":{
                "seg_time": 0.0
            },
            "parameters": {
                "every-nth-frame":2
            }
        }
        for item in seg_info["analytics"]:
            temp=request.copy()
            temp["source"]["uri"]=item["stream"]
            temp["tags"]["seg_time"]=item["seg_time"]
            print("Schedule analysis: "+temp["source"]["uri"], flush=True)
            if "initSeg" in seg_info:
                temp["source"]["uri-init"]=seg_info["initSeg"]
            self._producer.send(analytics_topic, json.dumps(temp))

    def transcode(self, user, seg_info, search_interval=10):
        request={
            "meta-db": {
                "stream": seg_info["stream"],
                "time_range": [
                    seg_info["transcode"]["seg_time"]-search_interval,
                    seg_info["transcode"]["seg_time"],
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
                "adpath": seg_info["transcode"]["stream"],
            },
            "user_info": {
                "name": user,
                "keywords": [] #"keywords": ["sports","animal"]
            }
        }
        self._producer.send(transcode_topic, json.dumps(request))

    def flush(self):
        self._producer.flush()
