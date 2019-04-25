#!/usr/bin/python3

import requests
import urllib.parse
import json
import time
import os
from optparse import OptionParser


video_analytics_service = "http://localhost:8080/pipelines/"
timeout = 30
sleep_for_status = 0.5

request_template = {
    "source": {
        "uri": "file:///home/video-analytics/samples/pinwheel.ts",
        "type": "uri"
    },
    "destination": {
        "uri": "file:///home/video-analytics/samples/results.txt",
        "type": "file"
    }
}

def get_options():
    parser = OptionParser()
    parser.add_option("--pipeline", action="store", dest="pipeline",
                      type="string", default='object_detection')
    parser.add_option("--source", action="store", dest="source",
                      type="string", default='file:///home/video-analytics/samples/pinwheel.ts')
    parser.add_option("--destination", action="store", dest="destination",
                      type="string", default='/home/video-analytics/samples/results.txt')

    return parser.parse_args()

def print_json(object):
    print(json.dumps(object,
                     sort_keys=True,
                     indent=4,
                     separators=[',',': ']))
    
def read_detection_results(destination):
    with open(destination) as file:
        for line in file:
            print("Detection Result: \n")
            print_json(json.loads(line))
            
def wait_for_pipeline(instance_id,
                      pipeline="object_detection",
                      version="1"):
    status = {"state":"RUNNING"}
    while((status["state"]=="RUNNING") or (status["state"]==None)):
        status=get_status(instance_id,pipeline,version)
        if (status==None):
            return
        print("Pipeline Status:\n")
        print_json(status)
        
        time.sleep(sleep_for_status)

def get_status(instance_id,
               pipeline="object_detection",
               version="1"):
    
    status_url = urllib.parse.urljoin(video_analytics_service,
                                      "/".join([pipeline,
                                                version,
                                                str(instance_id),"status"]))

    try:
        r = requests.get(status_url,timeout=timeout)
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            None
    except requests.exceptions.RequestException as e:
        return None
    
def start_pipeline(stream_uri,
                   pipeline,
                   destination,
                   version="1",
                   tags=None,
                   parameters=None):

    request = request_template
    request["source"]["uri"] = stream_uri

    try:
        os.remove(os.path.abspath(destination))
    except OSError:
        pass

    request["destination"]["uri"] = urllib.parse.urljoin("file://",os.path.abspath(destination))
    if (tags) and (len(tags) > 0):
        request["tags"] = tags
    if (parameters) and (len(parameters) > 0):
        request["parameters"] = parameters
    pipeline_url = urllib.parse.urljoin(video_analytics_service,
                                        pipeline+"/"+version)

    print("Starting Pipeline: %s" % (pipeline_url))

    try:
        r = requests.post(pipeline_url, json=request, timeout=timeout)
        if r.status_code == 200:
            instance_id = int(r.text)
            return instance_id
    except requests.exceptions.RequestException as e:
        return None
    

if __name__ == "__main__":
    try:
        options, args = get_options()
    except Exception as error:
        print(error)
        logger.error("Getopt Error!")
        exit(1)
    instance_id=start_pipeline(options.source,options.pipeline,options.destination)
    wait_for_pipeline(instance_id)
    read_detection_results(options.destination)
