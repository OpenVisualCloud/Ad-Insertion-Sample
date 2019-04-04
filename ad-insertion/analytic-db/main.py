#!/usr/bin/python3
#!/usr/bin/python3

from messaging import Consumer
from db import DataBase
import json
import time

kafka_topic = "seg_analytics_data"
kafka_group = "kafka_to_db_converter"

if __name__ == "__main__":
    db=DataBase()
    c=Consumer(kafka_group)
    while True:
        try:
            print("listening to messages")
            while True:
                data=[]
                start=time.clock()
                for msg in c.messages(kafka_topic,timeout=100):
                    if msg:
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
                            print("Ingest "+stream+": "+str(value["time"]),flush=True)
                            data.append((stream,value))
                        except Exception as e:
                            print(str(e))
                            print(value)

                    # batch write to DB every second or >500 in size
                    if (time.clock()-start>=0.5 and data) or len(data)>500:
                        db.save(data)
                        start=time.clock()
                        data=[]

        except Exception as e:
            print(str(e))
        time.sleep(10)
