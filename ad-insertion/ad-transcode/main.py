#!/usr/bin/python3

from messaging import Consumer
from zkstate import ZKState
from process import Process, ADTranscode
import time
from db import DataBase

kafka_topic="ad_transcode_sched"
kafka_group="ad_transcode_creator"

class TranscodeTask(Process):
    def __init__(self, cmdtype):
        super(TranscodeTask,self).__init__(cmdtype)
        self.cmdtype = cmdtype

def main():
    db = DataBase()
    consumer = Consumer(kafka_group)

    while True:
        try:
            print("ad transcode service: listening to messages", flush=True)
            for msg in consumer.messages(kafka_topic):
                print("ad transcode service: recieved message: " + str(msg), flush=True)
                ADTranscode(msg,db)
        except Exception as e:
            print(str(e))
            print("ad transcode exception in service")
        time.sleep(10)

if __name__ == "__main__":
    main()
