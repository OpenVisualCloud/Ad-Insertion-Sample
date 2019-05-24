#!/usr/bin/python3

from messaging import Consumer
import requests
import ast
from zkstate import ZKState
import merged_segment as merge

import json
import time
import os
import re

kafka_host = ["kafka:9092"]
kafka_topic = "seg_analytics_sched"
kafka_group = "video_analytics"

video_analytic_url = "http://localhost:8080/pipelines/"
timeout = 30
sleep_for_status = 0.1

analytic_rest_msg_template = {
    "source": {
        "uri": "",
        "type":"uri"
    },
    "destination": {
        "type": "kafka",
        "hosts": kafka_host,
        "topic": "seg_analytics_data"
    }
}


def start_analytic(stream_uri, pipeline, tags, parameters):
    jsonData = analytic_rest_msg_template
    jsonData['source']['uri'] = stream_uri

    if (tags) and (len(tags) > 0):
        jsonData["tags"] = tags
    if (parameters) and (len(parameters) > 0):
        jsonData["parameters"] = parameters

    url = video_analytic_url+pipeline
    try:
        r = requests.post(url, json=jsonData, timeout=timeout)
        print("VA feeder: response code on post request", flush=True)
        if r.status_code == 200:
            return r.text
        print("VA feeder: start_analytic: response message " + r.text, flush=True)
    except requests.exceptions.RequestException as e:
        print("VA feeder: Request failed : " + str(e))
    return None


def process_stream(streamstring):
    streamjson = ast.literal_eval(streamstring)
    if 'source' not in streamjson:
        print("VA feeder: missing source object in input ", flush=True)
        return
    if 'pipeline' not in streamjson:
        print("VA feeder: missing pipeline in input", flush=True)
        return
    if 'uri' not in streamjson['source']:
        print("VA feeder: missing uri in source", flush=True)
        return
    pipeline = streamjson["pipeline"]+"/1"
    tags = {}
    if 'tags' in streamjson:
        tags = streamjson["tags"]
    parameters = {}
    if 'parameters' in streamjson:
        parameters = streamjson["parameters"]

    stream = streamjson['source']['uri']
    print("VA feeder: stream: "+stream, flush=True)
    if not stream:
        print("VA feeder: empty uri", flush=True)
        return

    init_stream = None
    zk_path = None
    if 'uri-init' in streamjson['source']:
        init_stream = streamjson['source']['uri-init']
        print("VA feeder: init_stream: "+init_stream, flush=True)
        zk_path = stream+"/"+pipeline

    m1 = re.search("(.*)/.*_([0-9]+.ts)$", stream)
    if m1:
        segment = stream.split('/')[-1].split('_')[-1]
        zk_path = m1.group(1)+"/"+segment+"/"+pipeline

    print("VA feeder: zk_path "+zk_path, flush=True)
    zk = ZKState(zk_path)
    if zk.processed():
        print("VA feeder: " + stream + " already complete", flush=True)
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
        print("VA feeder: start analytic ", flush=True)
        instanceid = start_analytic(stream, pipeline, tags, parameters)
        if instanceid:
            print("VA feeder: waiting for analytics to complete for stream: " +
                  stream + " analytics-instance-id: "+instanceid, flush=True)
            while True:
                time.sleep(sleep_for_status)
                status, fps = get_analytic_status(instanceid.strip(), pipeline)
                print("VA feeder: segment status : " + status, flush=True)
                if status == 'COMPLETED':
                    print("VA feeder: Avg fps: " + str(fps), flush=True)
                    zk.process_end()
                    break
                elif status == 'RUNNING':
                    continue
                elif status == 'QUEUED':
                    continue
                else:
                    print("VA feeder: segment processing failed", flush=True)
                    zk.process_abort()
                    break
        if merged_segment:
            merge.delete_merged_segment(merged_segment)
    zk.close()


def get_analytic_status(instanceId, pipeline):
    try:
        r = requests.get(video_analytic_url+pipeline+"/" +
                         instanceId+"/status", timeout=timeout)
        if r.status_code == 200:
            jsonValue = r.json()
            return jsonValue.get('state'), jsonValue.get('avg_fps')
    except requests.exceptions.RequestException as e:
        print("VA feeder: Error in getting status " + str(e), flush=True)
    return "UNKNOWN", None


if __name__ == "__main__":
    c = Consumer(kafka_group)
    while True:
        try:
            print("VA feeder: listening to messages", flush=True)
            for msg in c.messages(kafka_topic):
                print("VA feeder: recieved message: " + str(msg), flush=True)
                try:
                    process_stream(msg)
                except Exception as e:
                    print("VA feeder: "+str(e), flush=True)
        except Exception as e:
            print("VA feeder: error in main" + str(e), flush=True)
        time.sleep(10)
