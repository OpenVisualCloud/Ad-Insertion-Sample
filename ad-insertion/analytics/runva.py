#!/usr/bin/python3

from vaserving.pipeline_manager import PipelineManager
from vaserving.model_manager import ModelManager
from concurrent.futures import ThreadPoolExecutor
from gi.repository import GLib
import time

class RunVA(object):
    def __init__(self):
        super(RunVA, self).__init__()
        ModelManager.load_config("/home/models",{})
        PipelineManager.load_config("/home/pipelines",1)
        self._maincontext=GLib.MainLoop().get_context()
        GLib.timeout_add(1000,self._noop)

    def _noop(self):
        return True

    def loop(self, reqs, pipeline, version="1"):
        print(reqs, flush=True)
        pid,msg=PipelineManager.create_instance(pipeline,version,reqs)
        if pid is None:
            print("Exception: "+str(msg), flush=True)
            return -1
        fps=0
        while True:
            self._maincontext.iteration()
            pinfo=PipelineManager.get_instance_status(pipeline,version,pid)
            print(pinfo, flush=True)
            if pinfo is not None: 
                state = pinfo["state"]
                if state == "COMPLETED":
                    fps=pinfo["avg_fps"]
                    print("Status analysis: Timing {0} {1} {2} {3} {4}".format(reqs["start_time"], pinfo["start_time"], pinfo["elapsed_time"], reqs["user"], reqs["source"]["uri"]), flush=True)
                    break
                if state == "ABORTED" or state == "ERROR": return -1

        PipelineManager.stop_instance(pipeline,version,pid)
        return fps
