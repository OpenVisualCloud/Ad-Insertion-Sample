from modules.Pipeline import Pipeline  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error
import string
import shlex
import subprocess
import tempfile
import time
import copy
from threading import Thread
import shutil

logger = logging.get_logger('FFmpegPipeline', is_static=True)

if shutil.which('ffmpeg') is None:
    raise Exception("ffmpeg not installed")


class FFmpegPipeline(Pipeline):

    def __init__(self, id, config, models):
        self.config = config
        self.models = models
        self.template = config['template']
        self.id = id
        self._process = None
        self.start_time = None
        self.stop_time = None
        self._ffmpeg_launch_string = None
        self.request = None
        self.state = None
        self.fps = None

    def stop(self):
        if self._process:
            self.state = "ABORTED"
            self._process.kill()
            logger.debug("Setting Pipeline {id} State to ABORTED".format(id=self.id))
 
    def params(self):
        request = copy.deepcopy(self.request)
        del(request["models"])

        params_obj = {
            "id": self.id,
            "request": request,
            "type": self.config["type"],
            "launch_command": self._ffmpeg_launch_string
        }

        return params_obj

    def status(self):
        logger.debug("Called Status")
        if self.stop_time is not None:
            elapsed_time = self.stop_time - self.start_time
        else:
            elapsed_time = time.time() - self.start_time

        status_obj = {
             "id": self.id,
             "state": self.state,
             "avg_fps": self.fps,
             "start_time": self.start_time,
             "elapsed_time": elapsed_time
         }

        return status_obj

    def _spawn(self,args):
        self.start_time = time.time()
        self._process=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        self.state = "RUNNING"
        self._process.poll()
        while self._process.returncode == None:
            next_line = self._process.stderr.readline()
            fps_idx = next_line.rfind('fps=')
            q_idx = next_line.rfind('q=')
            if fps_idx != -1 and q_idx != -1:
                self.fps = int(float(next_line[fps_idx+4:q_idx].strip()))
            self._process.poll()
        self.stop_time = time.time()
        if self.state != "ABORTED":
            if self._process.returncode == 0:
                self.state = "COMPLETED"
            else:
                self.state = "ERROR"
        self._process = None

    def _add_tags(self, iemetadata_args):
        if "tags" in self.request:
            try:
                for key in self.request["tags"]:
                    iemetadata_args.append("-custom_tag")
                    iemetadata_args.append("%s:%s," % (key, self.request["tags"][key]))
                if len(iemetadata_args):
                    # remove final comma
                    iemetadata_args[-1] = iemetadata_args[-1][:-1]
            except Exception:
                logger.error("Error adding tags")

    def _add_default_parameters(self):
        request_parameters = self.request.get("parameters", {})
        pipeline_parameters = self.config.get("parameters", {})

        for key in pipeline_parameters:
            if (not key in request_parameters) and ("default" in pipeline_parameters[key]):
                request_parameters[key] = pipeline_parameters[key]["default"]

        self.request["parameters"] = request_parameters

    def start(self, request):
        logger.debug("Starting Pipeline {id}".format(id=self.id))
        self.request = request
        request["models"] = self.models

        self._add_default_parameters()
        self._ffmpeg_launch_string = string.Formatter().vformat(self.template, [], request)
        args = ['ffmpeg']
        args.extend(shlex.split(self._ffmpeg_launch_string))
        iemetadata_args = ["-f", "iemetadata", "-source_url", self.request["source"]["uri"]]

        self._add_tags(iemetadata_args)

        if 'destination' in request:
            if request['destination']['type'] == "kafka":
                for item in request['destination']['hosts']:
                    iemetadata_args.append("kafka://"+item+"/"+request["destination"]["topic"])
            elif request['destination']['type'] == "file":
                iemetadata_args.append(request['destination']['uri'])
        else:
            iemetadata_args.append("file:///" + tempfile.mktemp(".json"))
                                    
        args.extend(iemetadata_args)
        logger.debug(args)
        thread = Thread(target=self._spawn, args=[args])
        thread.start()    
