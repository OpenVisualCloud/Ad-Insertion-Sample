#!/usr/bin/python3

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NodeExistsError
from kazoo.protocol.states import KazooState
import traceback
import time

ZK_HOSTS='zookeeper-service:2181'

class ZKState(object):
    def __init__(self):
        super(ZKState,self).__init__()
        self._zk=None

    def set_path(self, path, name=None):
        if self._zk is None:
            options={"max_tries":-1,"max_delay":5,"ignore_expire":True}
            self._zk=KazooClient(hosts=ZK_HOSTS,connection_retry=options)
            try:
                self._zk.start(timeout=3*3600)
            except:
                print(traceback.format_exc(), flush=True)

        self._path=path
        self._name="" if name is None else name+"."
        self._zk.retry(self._zk.ensure_path,path)

    def processed(self):
        return self._zk.retry(self._zk.exists, self._path+"/"+self._name+"complete")
        
    def process_start(self):
        if self.processed(): return False
        try:
            self._zk.create(self._path+"/"+self._name+"processing",ephemeral=True)
            return True
        except NodeExistsError: # another process wins
            return False

    def process_end(self):
        try:
            self._zk.retry(self._zk.create,self._path+"/"+self._name+"complete")
        except NodeExistsError:
            pass
        self._zk.delete_async(self._path+"/"+self._name+"processing")

    def process_abort(self):
        self._zk.delete_async(self._path+"/"+self._name+"processing")

    def close(self):
        self._zk.stop()
        self._zk.close()
        self._zk=None
