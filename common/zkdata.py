#!/usr/bin/python3

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NodeExistsError
import traceback
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
            try:
                self._zk.start(timeout=3*3600)
            except:
                print(traceback.format_exc(), flush=True)

    def _set_set_cb(self, ao):
        try:
            ao.get()
        except:
            print(traceback.format_exc(), flush=True)
            self._set_set(ao.arg_path,ao.arg_value)

    def _set_set(self, path, value):
        ao=self._zk.set_async(path,value)
        ao.arg_path=path
        ao.arg_value=value
        ao.rawlink(self._set_set_cb)

    def _set_create_cb(self, ao):
        try:
            ao.get()
        except NodeExistsError:
            self._zk.set_async(ao.arg_path,ao.arg_value)
        except:
            print(traceback.format_exc(), flush=True)
            self.set(ao.arg_path, ao.arg_value)

    def set(self, path, value):
        self._connect()
        value=json.dumps(value).encode('utf-8')
        ao=self._zk.create_async(path,value,makepath=True)
        ao.arg_path=path
        ao.arg_value=value
        ao.rawlink(self._set_create_cb)

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
