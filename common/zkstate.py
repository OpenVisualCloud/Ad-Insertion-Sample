#!/usr/bin/python3

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NodeExistsError

ZK_HOSTS='zookeeper-service:2181'

class ZKState(object):
    def __init__(self, path, name=None, timeout=30):
        super(ZKState,self).__init__()
        self._zk=KazooClient(hosts=ZK_HOSTS, timeout=timeout)
        self._zk.start(timeout=timeout)
        self._path=path
        self._name=""
        if name != None:
            self._name=name+"."
        self._zk.ensure_path(path)

    def processed(self):
        return self._zk.exists(self._path+"/"+self._name+"complete")
        
    def process_start(self):
        if self.processed(): return False
        if self._zk.exists(self._path+"/"+self._name+"processing"): return False
        try:
            self._zk.create(self._path+"/"+self._name+"processing",ephemeral=True)
            return True
        except NodeExistsError: # another process wins
            return False

    def process_end(self):
        self._zk.create(self._path+"/"+self._name+"complete")
        self._zk.delete(self._path+"/"+self._name+"processing")

    def process_abort(self):
        try:
            self._zk.delete(self._path+"/"+self._name+"processing")
        except NoNodeError:
            pass

    def close(self):
        self._zk.stop()
        self._zk.close()
