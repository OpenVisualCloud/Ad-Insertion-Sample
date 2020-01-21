#!/usr/bin/python3

from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError, NodeExistsError
import time

ZK_HOSTS='zookeeper-service:2181'

class ZKState(object):
    def __init__(self, path, name=None):
        super(ZKState,self).__init__()
        self._zk=KazooClient(hosts=ZK_HOSTS)
        while True:
            try:
                self._zk.start()
                break
            except Exception as e:
                print("Exception: "+str(e), flush=True)
                time.sleep(5)
        self._path=path
        self._name="" if name is None else name+"."
        self._zk.ensure_path(path)

    def processed(self):
        return self._zk.retry(self._zk.exists, self._path+"/"+self._name+"complete")
        
    def process_start(self):
        if self.processed(): return False
        if self._zk.exists(self._path+"/"+self._name+"processing"): return False
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
        self._zk.delete(self._path+"/"+self._name+"processing")

    def process_abort(self):
        try:
            self._zk.retry(self._zk.delete,self._path+"/"+self._name+"processing")
        except NoNodeError:
            pass

    def close(self):
        self._zk.stop()
        self._zk.close()
