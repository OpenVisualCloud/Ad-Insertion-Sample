#!/usr/bin/python3

import requests
import hashlib
import time
import json

class DataBase(object):
    def __init__(self, index="analytics"):
        super(DataBase,self).__init__()
        self._host="http://database-service:9200"
        self._index=index
        self._type="_doc"
        self._template=False
        self._stream="_stream"

    def _digest(self, name):
        return hashlib.sha224(name.encode('utf-8')).hexdigest()

    def _create_bulk(self, analytics):
        cmds=[]
        for item in analytics:
            cmds.append({"index":{"_index":self._index,"_type":self._type}})
            item[1]["_stream"]=self._digest(item[0])
            cmds.append(item[1])
            if len(cmds)>=200:
                yield cmds
                cmds=[]
        if cmds: yield cmds
        
    def save(self, analytics):
        ''' Builk save anlytics data to database
            analytics: list of analytic-data
        '''
        if not self._template:
            # initialize the DB to have zero replica
            requests.put(self._host+"/_template/zero",json={
                "index_patterns": "*",
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas":0,
                }
            })
            self._template=True

        for chunk in self._create_bulk(analytics):
            cmds="\n".join([json.dumps(x) for x in chunk])+"\n"
            r=requests.post(self._host+"/_bulk",data=cmds,headers={"content-type":"application/x-ndjson"})
            if r.status_code!=200 and r.status_code!=201:
                print(r.json(), flush=True)
        
    def query(self,stream,time_range,time_field="time"):
        ''' Query time period for analytics data

            stream: the stream name
            time_range: the timestamp range
            time_field: optionally specify the timestamp field name
        '''
        _query={
            "query": {
                "bool": {
                    "must": [{
                            "match": {
                                self._stream: self._digest(stream),
                            },
                        },{
                            "range": {
                                time_field: {
                                    "gte": time_range[0],
                                    "lte": time_range[1],
                                }
                            }
                        }
                    ]
                }
            }
        }
        r=requests.post(self._host+"/"+self._index+"/"+self._type+"/_search",json=_query)
        if r.status_code!=200: return []
        r=r.json()
        if "status" in r: return []
        return [x["_source"] for x in r["hits"]["hits"]]

