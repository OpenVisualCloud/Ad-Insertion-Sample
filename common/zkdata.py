#!/usr/bin/python3

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NodeExistsError
import json
import time

ZK_HOSTS='zookeeper-service:2181'

class ZKData(object):
    def __init__(self):
        super(ZKData,self).__init__()
        self._zk=None

    def _connect(self):
        if self._zk is None: 
            self._zk=KazooClient(hosts=ZK_HOSTS)
            while True:
                try:
                    self._zk.start()
                    return
                except Exception as e:
                    print("Exception: "+str(e), flush=True)
                    time.sleep(5)

    def set(self, path, value):
        self._connect()
        value=json.dumps(value).encode('utf-8')
        if self._zk.retry(self._zk.exists,path):
            try:
                self._zk.retry(self._zk.set,path,value)
                return
            except NoNodeError:
                pass
        try:
            self._zk.retry(self._zk.create,path,value,makepath=True)
        except NodeExistsError:
            pass

    def get(self, path):
        self._connect()
        try:
            value, stat= self._zk.retry(self._zk.get,path)
            if not value: return {}
            return json.loads(value.decode('utf-8'))
        except Exception as e:
            return {}

    def close(self):
        if self._zk:
            self._zk.stop()
            self._zk.close()
