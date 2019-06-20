import string
import json
import time
import os
import copy
import modules.Destination as Destination  # pylint: disable=import-error
from modules.Pipeline import Pipeline  # pylint: disable=import-error
import modules.GstGVAJSONMeta as GstGVAJSONMeta  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error

import gi  # pylint: disable=import-error
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject  # pylint: disable=import-error

logger = logging.get_logger('GSTPipeline', is_static=True)


class GStreamerPipeline(Pipeline):

    Gst.init(None)
    GObject.threads_init()

    def __init__(self, id, config, models):
        self.config = config
        self.id = id
        self.pipeline = None
        self.template = config['template']
        self.models = models
        self.request = None
        self.state = None
        self.frame_count = 0
        self.start_time = None
        self.stop_time = None
        self.avg_fps = 0
        self.destination = None
        self._gst_launch_string = None
        self.latency_times = dict()
        self.sum_pipeline_latency = 0
        self.count_pipeline_latency = 0

    def stop(self):
        if self.pipeline is not None:
            self.pipeline.set_state(Gst.State.NULL)
            if self.state is "RUNNING":
                self.state = "ABORTED"
                logger.debug("Setting Pipeline {id} State to ABORTED".format(id=self.id))

            self.stop_time = time.time()

        del self.pipeline
        self.pipeline = None

        return self.status()

    def params(self):

        request = copy.deepcopy(self.request)
        del request["models"]

        params_obj = {
            "id": self.id,
            "request": request,
            "type": self.config["type"],
            "launch_command": self._gst_launch_string
        }

        return params_obj

    def status(self):

        logger.debug("Called Status")
        if self.stop_time is not None:
            elapsed_time = self.stop_time - self.start_time
        else:
            elapsed_time = time.time() - self.start_time
        if self.count_pipeline_latency == 0:
            avg_pipeline_latency = 0
        else:
            avg_pipeline_latency = self.sum_pipeline_latency / self.count_pipeline_latency
        status_obj = {
            "id": self.id,
            "state": self.state,
            "avg_fps": self.avg_fps,
            "start_time": self.start_time,
            "elapsed_time": elapsed_time,
            "avg_pipeline_latency": avg_pipeline_latency
        }

        return status_obj

    def get_avg_fps(self):
        return self.avg_fps

    def _add_tags(self):
        if "tags" in self.request:
            metaconvert = self.pipeline.get_by_name("jsonmetaconvert")
            if metaconvert:
                metaconvert.set_property("tags", json.dumps(self.request["tags"]))
            else:
                logger.debug("tags given but no metaconvert element found")

    def _add_default_parameters(self):
        request_parameters = self.request.get("parameters", {})
        pipeline_parameters = self.config.get("parameters", {})

        for key in pipeline_parameters:
            if (not key in request_parameters) and ("default" in pipeline_parameters[key]):
                request_parameters[key] = pipeline_parameters[key]["default"]

        self.request["parameters"] = request_parameters

    def _add_element_parameters(self):
        request_parameters = self.request.get("parameters", {})
        pipeline_parameters = self.config.get("parameters", {})

        for key in pipeline_parameters:                
            if "element" in pipeline_parameters[key]:
                if key in request_parameters:
                    element = self.pipeline.get_by_name(pipeline_parameters[key]["element"])
                    if element:
                        element.set_property(key, request_parameters[key])
                    else:
                        logger.debug("parameter given for element but no element found")

    def calculate_times(self,sample):
        buffer = sample.get_buffer()
        segment = sample.get_segment()
        times={}
        times['segment.time'] = segment.time
        times['segment.start'] = segment.start
        times['segment.base'] = segment.base
        times['segment.position'] = segment.position
        times['buffer.pts'] = buffer.pts
        times['buffer.dts'] = buffer.dts
        times['buffer.duration'] = buffer.duration
        times['pipeline.base_time'] = self.pipeline.base_time
        times['stream_time'] = segment.to_stream_time(Gst.Format.TIME,buffer.pts)                
        times['running_time'] = segment.to_running_time(Gst.Format.TIME,buffer.pts)
        times['clock_time'] = times['running_time'] + self.pipeline.base_time

        return times
        

    def record_format_location_callback (self,splitmux, fragment_id,sample,data=None):
        times=self.calculate_times(sample)

        if (self._real_base == None):
            clock = Gst.SystemClock(clock_type=Gst.ClockType.REALTIME)
            self._real_base = clock.get_time()
            self._stream_base = times["segment.time"]
            metaconvert = self.pipeline.get_by_name("jsonmetaconvert")
            
            if metaconvert:
                if ("tags" not in self.request):
                    self.request["tags"]={}
                self.request["tags"]["real_base"] = self._real_base
                self.request["tags"]["stream_base"] = self._stream_base
                self.request["tags"]["pts_base"] = times["buffer.pts"]
                metaconvert.set_property("tags", json.dumps(self.request["tags"]))

        adjusted_time = self._real_base + (times["stream_time"] - self._stream_base)
        self._year_base = time.strftime("%Y", time.localtime(adjusted_time / 1000000000))
        self._month_base = time.strftime("%m", time.localtime(adjusted_time / 1000000000))
        self._day_base = time.strftime("%d", time.localtime(adjusted_time / 1000000000))
        self._dirName = "%s/%s/%s/%s" %(self.request["parameters"]["recording_prefix"],self._year_base,self._month_base,self._day_base)

        try:
            os.makedirs(self._dirName)
        except FileExistsError:
            print("Directory already exists")

        return "%s/:real_base:%d:stream_base:%d:stream_time:%d_.mp4" %(self._dirName,
                                                                     self._real_base,
                                                                     self._stream_base,
                                                                     times["stream_time"])

        # uncomment for full information debug
        #return "%s:base:%d:clock:%d:stream:%d:pts:%d:dur:%d.mp4"%(splitmux.get_property("location"),
         #                            times['pipeline.base_time'],
          #                           times['clock_time'],
           #                          times['stream_time'],
            #                         times['buffer.pts'],
             #                        times['buffer.duration'])

    def start(self, request):
        logger.debug("Starting Pipeline {id}".format(id=self.id))
        self.request = request

        try:
            self.destination = Destination.create_instance(request)
        except:
            self.destination = None

        request["models"] = self.models

        self._add_default_parameters()
        
        self._gst_launch_string = string.Formatter().vformat(self.template, [], request)

        logger.debug(self._gst_launch_string)

        self.pipeline = Gst.parse_launch(self._gst_launch_string)

        self._add_element_parameters()
        self._add_tags()

        sink = self.pipeline.get_by_name("appsink")
        src = self.pipeline.get_by_name("urisource")
        if src and sink:
            src.connect("pad-added", GStreamerPipeline.source_pad_added_callback, self)
            sink_pad = sink.get_static_pad("sink")
            sink_pad.add_probe(Gst.PadProbeType.BUFFER, GStreamerPipeline.appsink_probe_callback, self)
        
        sink.set_property("emit-signals", True)
        sink.set_property('sync', False)
        sink.connect("new-sample", GStreamerPipeline.on_sample, self)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", GStreamerPipeline.bus_call, self)

        record = self.pipeline.get_by_name("record")
        self._real_base=None
        if (record != None):
            
            record.connect("format-location-full",
                           self.record_format_location_callback,
                           None)

            #clock = Gst.SystemClock(clock_type=Gst.ClockType.REALTIME)
            #self.pipeline.use_clock(clock)
        
        self.pipeline.set_state(Gst.State.PLAYING)
        self.start_time = time.time()

    @staticmethod
    def source_pad_added_callback(element, pad, self):
        pad.add_probe(Gst.PadProbeType.BUFFER, GStreamerPipeline.urisource_probe_callback, self)
        return Gst.FlowReturn.OK
        

    @staticmethod
    def urisource_probe_callback(pad, info, self):
        buffer = info.get_buffer()
        pts = buffer.pts
        self.latency_times[pts] = time.time()
        return Gst.PadProbeReturn.OK

    @staticmethod
    def appsink_probe_callback(pad, info, self):
        buffer = info.get_buffer()
        pts = buffer.pts
        source_time = self.latency_times.pop(pts, -1)
        if not source_time == -1:
            self.sum_pipeline_latency += time.time() - source_time
            self.count_pipeline_latency += 1
        return Gst.PadProbeReturn.OK


    @staticmethod
    def on_sample(sink, self):

        logger.debug("Received Sample from Pipeline {id}".format(id=self.id))
        sample = sink.emit("pull-sample")
        try:

            buf = sample.get_buffer()
            try:
                meta = buf.get_meta("GstGVAJSONMetaAPI")
            except:
                meta = None

            if meta is None:
                logger.debug("No GstGVAJSONMeta")
            else:
                json_string = GstGVAJSONMeta.get_json_message(meta).decode('utf-8')  # pylint: disable=undefined-variable
                json_object = json.loads(json_string)
                #json_object['tags']={'times':self.calculate_times(sample)}
                logger.debug(json.dumps(json_object))
                if self.destination and ("objects" in json_object) and (len(json_object["objects"]) > 0):
                    self.destination.send(json_object)
        except Exception as error:
            logger.error("Error on Pipeline {id}: {err}".format(id=self.id, err=error))

        self.frame_count += 1
        self.avg_fps = self.frame_count/(time.time()-self.start_time)

        return Gst.FlowReturn.OK

    @staticmethod
    def bus_call(bus, message, self):
        t = message.type
        if t == Gst.MessageType.EOS:
            logger.info("Pipeline {id} Ended".format(id=self.id))
            self.pipeline.set_state(Gst.State.NULL)
            if self.state is "RUNNING":
                logger.debug("Setting Pipeline {id} State to COMPLETED".format(id=self.id))
                self.state = "COMPLETED"

            self.stop_time = time.time()
            if (self.destination):
                del self.destination
                self.destination=None
            del self.pipeline
            self.pipeline = None
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            logger.error("Error on Pipeline {id}: {err}".format(id=id, err=err))

            if (self.state is None) or (self.state is "RUNNING"):
                logger.debug("Setting Pipeline {id} State to ERROR".format(id=self.id))
                self.state = "ERROR"
        elif t == Gst.MessageType.STATE_CHANGED:
            old_state, new_state, pending_state = message.parse_state_changed()
            if message.src == self.pipeline:
                if old_state == Gst.State.PAUSED and new_state == Gst.State.PLAYING:
                    if self.state is None:
                        logger.debug("Setting Pipeline {id} State to RUNNING".format(id=self.id))
                        self.state = "RUNNING"

        else:
            pass
        return True
