#!/usr/bin/python3

from modules.PipelineManager import PipelineManager
from modules.ModelManager import ModelManager
from concurrent.futures import ThreadPoolExecutor
from gi.repository import GObject

class RunVA(object):
    def __init__(self):
        super(RunVA, self).__init()
        ModelManager.load_config("/home/models",{})
        PipelineManager.load_config("/home/pipelines",1)
        self._ml=None
        self._threadpool=ThreadPoolExecutor(1)
        self._threadpool.submit(self._mainloop)

    def _mainloop(self):
        try:
            self._ml=GObject.MainLoop()
            self._ml.run()
        except Exception as e:
            print("Exception: "+str(e), flush=True)

    def loop(self, reqs, pipeline, version="1"):
        pid,msg=PipelineManager.create_instance(pipeline,version,reqs)
        if pid is None:
            print("Exception: "+str(msg), flush=True)
            return -1

        fps=0
        while True:
            pinfo=PipelineManager.get_instance_status(pipeline,version,pid)
            if pinfo is not None: 
                state = pinfo["state"]
                if state == "COMPLETED": break
                if state == "ABORTED" or state == "ERROR": return -1
                fps=pinfo["avg_fps"]
            time.sleep(0.1)

        PipelineManager.stop_instance(pipeline,version,pid)
        return fps

    def close(self):
        if self._ml: self._ml.quit()
        self._threadpool.shutdown()
