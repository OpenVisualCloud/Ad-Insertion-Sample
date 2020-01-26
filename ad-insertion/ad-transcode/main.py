#!/usr/bin/python3

from messaging import Consumer
from zkstate import ZKState
from zkdata import ZKData
from process import ADTranscode
from db import DataBase
import traceback
import time

kafka_topic="ad_transcode_sched"
kafka_group="ad_transcode_creator"

db = DataBase()
consumer = Consumer(kafka_group)
zks = ZKState()
zkd = ZKData()

while True:
    try:
        print("ad transcode service: listening to messages", flush=True)
        for msg in consumer.messages(kafka_topic):
            ADTranscode(zks,zkd,msg,db)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    time.sleep(10)

zks.close()
zkd.close()
consumer.close()
db.close()
