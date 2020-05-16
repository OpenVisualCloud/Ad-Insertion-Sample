#!/usr/bin/python3

from vaserving.vaserving import VAServing
from vaserving.pipeline import Pipeline
import time

class RunVA(object):
    def __init__(self):
        super(RunVA, self).__init__()
        vaserving_args = {
            'model_dir': '/home/models',
            'pipeline_dir': '/home/pipelines',
            'max_running_pipelines': 1,
        }
        print("vaserving args: {} ".format(vaserving_args),flush=True)
        VAServing.start(vaserving_args)
        self._pause = 0.05

    def loop(self, reqs, _pipeline, _version="1"):
        pipeline = VAServing.pipeline(_pipeline, _version)
        instance_id = pipeline.start(source=reqs["source"],
                                     destination=reqs["destination"],
                                     tags=reqs["tags"],
                                     parameters=reqs["parameters"])
        if instance_id is None:
            print("Pipeline {} version {} Failed to Start".format(
                _pipeline, _version), flush=True)
            return -1

        fps = 0
        while True:
            status = pipeline.status()
            print(status, flush=True)

            if (status.state.stopped()):

                print("Pipeline {} Version {} Instance {} Ended with {}".format(
                    _pipeline, _version, instance_id, status.state.name), flush=True)

                if status.state is Pipeline.State.COMPLETED:
                    fps = status.avg_fps
                    print("Status analysis: Timing {0} {1} {2} {3} {4}".format(
                        reqs["start_time"], status.start_time, status.elapsed_time, reqs["user"], reqs["source"]["uri"]), flush=True)
                    break

                if status.state is Pipeline.State.ABORTED or status.state is Pipeline.State.ERROR:
                    return -1
            time.sleep(self._pause)

        pipeline.stop()
        print("exiting va pipeline", flush=True)
        return fps

    def close(self):
        VAServing.stop()
