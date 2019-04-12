import os
import json
import common.settings  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error
import time
from modules.ModelManager import ModelManager  # pylint: disable=import-error


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

    pipelines = None
    logger = logging.get_logger('PipelineManager', is_static=True)

    pipeline_types = import_pipeline_types(logger)
    pipeline_instances = {}
    pipeline_state = {}
    pipeline_id = 0

    @staticmethod
    def load_config(pipeline_dir):
        PipelineManager.logger.info("Loading Pipelines from Config Path {path}".format(path=pipeline_dir))
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
        params_obj = {
            "name": name,
            "version":version,
            "type": PipelineManager.pipelines[name][version]["type"],
            "description": PipelineManager.pipelines[name][version]["description"],
        }

        if "parameters" in PipelineManager.pipelines[name][version]:
            params_obj["parameters"] = PipelineManager.pipelines[name][version]["parameters"]

        return params_obj

    @staticmethod
    def create_instance(name, version):
        PipelineManager.logger.info("Creating Instance of Pipeline {name}/{v}".format(name=name, v=version))

        try:
            pipeline_type = PipelineManager.pipelines[name][str(version)]['type']
            PipelineManager.pipeline_id += 1
            PipelineManager.pipeline_instances[PipelineManager.pipeline_id] = \
                PipelineManager.pipeline_types[pipeline_type](PipelineManager.pipeline_id,
                                                              PipelineManager.pipelines[name][str(version)],
                                                              ModelManager.models)

            return PipelineManager.pipeline_instances[PipelineManager.pipeline_id]
        except Exception as e:
            PipelineManager.logger.error(e)
            return None

    @staticmethod
    def get_instance_parameters(instance_id):
        return PipelineManager.pipeline_instances[instance_id].params()

    @staticmethod
    def get_instance_status(instance_id):
        return PipelineManager.pipeline_instances[instance_id].status()

    @staticmethod
    def stop_instance(instance_id):
        return PipelineManager.pipeline_instances[instance_id].stop()
