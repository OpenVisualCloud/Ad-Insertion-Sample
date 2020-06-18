#!/usr/bin/python3
#!/usr/bin/python3

from messaging import Consumer
from db import DataBase
from threading import Thread, Condition
import json
import time
import os

kafka_topic = "seg_analytics_data"
kafka_group = "kafka_to_db_converter"

class KafkaToDB(object):
    def __init__(self):
        super(KafkaToDB,self).__init__()
        self._db=DataBase()
        self._cache=[]
        self._cond=Condition()
        Thread(target=self._ingest).start()

    def _ingest(self):
        while True:
            self._cond.acquire()
            self._cond.wait()
            bulk=self._cache
            self._cache=[]
            self._cond.release()

            try:
                self._db.save(bulk)
                print("SaveToDB #"+str(len(bulk)), flush=True)
            except Exception as e:
                print("Exception: "+str(e), flush=True)

    def _send(self, data):
        self._cond.acquire()
        self._cache.append(data)
        self._cond.notify()
        self._cond.release()

    def listen(self):
        while True:
            print("listening to messages")
            try:
                c=Consumer(kafka_group)
                for msg in c.messages(kafka_topic):
                    try:
                        value=json.loads(msg)
                        value["time"]=float(value["timestamp"])/1.0e9
                        if "tags" in value:
                            if "seg_time" in value["tags"]:
                                value["time"]=value["time"]+float(value["tags"]["seg_time"])
                        if "tag" in value:
                            if "seg_time" in value["tag"]:
                                value["time"]=value["time"]+float(value["tag"]["seg_time"])
                        stream=value["source"].split("/")[-2]
                        self._send((stream, value))

                    except Exception as e:
                        print("Exception: "+str(e), flush=True)
            except Exception as e:
                print("Exception: "+str(e), flush=True)
                time.sleep(2)

k2d=KafkaToDB()
k2d.listen()

