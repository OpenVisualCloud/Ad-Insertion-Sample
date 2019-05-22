import os
import json
import common.settings  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error
import time
from http import HTTPStatus
from modules.ModelManager import ModelManager  # pylint: disable=import-error
from collections import deque


def import_pipeline_types(logger):
    pipeline_types = {}
    try:
        from modules.GStreamerPipeline import GStreamerPipeline  # pylint: disable=import-error
        pipeline_types['GStreamer'] = GStreamerPipeline
    except Exception as error:
        logger.error("Error loading GStreamer: %s\n" %(error,))
    try:
        from modules.FFmpegPipeline import FFmpegPipeline  # pylint: disable=import-error
        pipeline_types['FFmpeg'] = FFmpegPipeline
    except Exception as error:
        logger.error("Error loading FFmpeg: %s\n"%(error,))

    return pipeline_types


class PipelineManager:
    MAX_RUNNING_PIPELINES = -1

    currently_running_pipelines = 0
    logger = logging.get_logger('PipelineManager', is_static=True)
    pipeline_types = {}
    pipeline_instances = {}
    pipeline_state = {}
    pipeline_id = 0
    pipelines = None
    pipeline_queue = deque()

    @staticmethod
    def load_config(pipeline_dir, max_running_pipelines):
        PipelineManager.pipeline_types = import_pipeline_types(PipelineManager.logger)
        PipelineManager.logger.info("Loading Pipelines from Config Path {path}".format(path=pipeline_dir))
        PipelineManager.MAX_RUNNING_PIPELINES = max_running_pipelines
        pipelines = {}

        for root, subdirs, files in os.walk(pipeline_dir):

            if os.path.abspath(root) == os.path.abspath(pipeline_dir):
                for subdir in subdirs:
                    pipelines[subdir] = {}

            else:
                if len(files) == 0:
                    pipeline = os.path.basename(root)
                    pipelines[pipeline] = {}
                    for subdir in subdirs:
                        pipelines[pipeline][subdir] = {}
                else:
                    pipeline = os.path.basename(os.path.dirname(root))
                    version = os.path.basename(root)
                    for file in files:
                        path = os.path.join(root, file)
                        if path.endswith(".json"):
                            with open(path, 'r') as jsonfile:
                                config = json.load(jsonfile)
                                if ('type' not in config) or ('description' not in config):
                                    continue
                                if config['type'] in PipelineManager.pipeline_types:
                                    pipelines[pipeline][version] = config
                                else:
                                    del pipelines[pipeline][version]
                                    PipelineManager.logger.error(
                                        "Pipeline %s with type %s not supported" % (pipeline, config['type']))

        # Remove pipelines with no valid versions
        pipelines = dict([(model, versions) for model, versions in pipelines.items() if len(versions) > 0])
        PipelineManager.pipelines = pipelines

        PipelineManager.logger.info("Completed Loading Pipelines")

    @staticmethod
    def get_loaded_pipelines():
        result = []
        if PipelineManager.pipelines is not None:
            for pipeline in PipelineManager.pipelines:
                for version in PipelineManager.pipelines[pipeline]:
                    result.append(PipelineManager.get_pipeline_parameters(pipeline, version))

        return result

    @staticmethod
    def get_pipeline_parameters(name, version):
        try:
            params_obj = {
                "name": name,
                "version":version,
                "type": PipelineManager.pipelines[name][version]["type"],
                "description": PipelineManager.pipelines[name][version]["description"],
            }

            if "parameters" in PipelineManager.pipelines[name][version]:
                params_obj["parameters"] = PipelineManager.pipelines[name][version]["parameters"]

            return params_obj
        except Exception as e:
            PipelineManager.logger.error(e)
            return ('Invalid Pipeline or Version', HTTPStatus.BAD_REQUEST)

    @staticmethod
    def create_instance(name, version, request):
        PipelineManager.logger.info("Creating Instance of Pipeline {name}/{v}".format(name=name, v=version))

        try:
            pipeline_type = PipelineManager.pipelines[name][str(version)]['type']
            PipelineManager.pipeline_id += 1
            PipelineManager.pipeline_instances[PipelineManager.pipeline_id] = \
                PipelineManager.pipeline_types[pipeline_type](PipelineManager.pipeline_id,
                                                              PipelineManager.pipelines[name][str(version)],
                                                              ModelManager.models,
                                                              request)
            PipelineManager.pipeline_queue.append(PipelineManager.pipeline_id)
            PipelineManager.start()
            return PipelineManager.pipeline_id
        except Exception as e:
            PipelineManager.logger.error(e)
            return None
    
    @staticmethod
    def start():
        if (PipelineManager.MAX_RUNNING_PIPELINES <= 0 or PipelineManager.currently_running_pipelines < PipelineManager.MAX_RUNNING_PIPELINES) and len(PipelineManager.pipeline_queue) != 0:
            pipeline_to_start = PipelineManager.pipeline_instances[PipelineManager.pipeline_queue.popleft()]
            if(pipeline_to_start is not None):
                PipelineManager.currently_running_pipelines += 1
                pipeline_to_start.start()
        
    @staticmethod
    def start_queued():
        PipelineManager.currently_running_pipelines -= 1
        PipelineManager.start()

    @staticmethod
    def remove_from_queue(id):
        PipelineManager.pipeline_queue.remove(id)

    @staticmethod
    def get_instance_parameters(instance_id):
        if instance_id in PipelineManager.pipeline_instances:
            return PipelineManager.pipeline_instances[instance_id].params()
        return ('Invalid Pipeline Identifier', HTTPStatus.BAD_REQUEST)

    @staticmethod
    def get_instance_status(instance_id):
        if instance_id in PipelineManager.pipeline_instances:
            return PipelineManager.pipeline_instances[instance_id].status()
        return ('Invalid Pipeline Identifier', HTTPStatus.BAD_REQUEST)

    @staticmethod
    def stop_instance(instance_id):
        if instance_id in PipelineManager.pipeline_instances:
            return PipelineManager.pipeline_instances[instance_id].stop()
        return ('Invalid Pipeline Identifier', HTTPStatus.BAD_REQUEST)
