#!/usr/bin/python3

from messaging import Producer
import socket
import datetime
import psutil
import time
import json
import sys

kafka_topic="workloads"

if __name__ == "__main__":
    prefix="";
    if len(sys.argv)>1: prefix=sys.argv[1]
    instance=socket.gethostname()[0:3]
    machine=prefix+instance

    while True:
        try:
            p=Producer()
            while True:
                p.send(kafka_topic,json.dumps({
                    "time":datetime.datetime.utcnow().isoformat(),
                    "machine": machine,
                    "workload": psutil.cpu_percent(),
                }));
                time.sleep(1);
            p.close()
        except Exception as e:
            print(str(e))
        time.sleep(2)
