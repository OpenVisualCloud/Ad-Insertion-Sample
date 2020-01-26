#!/usr/bin/python3

from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import NoNodeError, NodeExistsError
import traceback
import json
import time

ZK_HOSTS='zookeeper-service:2181'

class ZKData(object):
    def __init__(self):
        super(ZKData,self).__init__()
        options={"max_tries":-1,"max_delay":5,"ignore_expire":True}
        self._zk=KazooClient(hosts=ZK_HOSTS,connection_retry=options)
        try:
            self._zk.start(timeout=3600)
        except:
            print(traceback.format_exc(), flush=True)

    def set(self, path, value):
        value=json.dumps(value).encode('utf-8')
        try:
            self._zk.create(path, value, makepath=True)
        except NodeExistsError:
            self._zk.set(path,value)

    def get(self, path):
        try:
            value, stat= self._zk.get(path)
            if not value: return {}
            return json.loads(value.decode('utf-8'))
        except Exception as e:
            return {}

    def close(self):
        self._zk.stop()
        self._zk.close()
