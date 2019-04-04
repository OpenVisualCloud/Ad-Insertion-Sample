import os
import json
import common.settings  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error


class ModelManager:
    models = None

    logger = logging.get_logger('ModelManager', is_static=True)
 
    @staticmethod
    def load_config(model_dir):
        ModelManager.logger.info("Loading Models from Config Path {path}".format(path=os.path.abspath(model_dir)))
        models = {}

        for path in os.listdir(model_dir):
            try:
                full_path = os.path.join(model_dir, path)
                if os.path.isdir(full_path):
                    model = path
                    for version_dir in os.listdir(full_path):
                        version_path = os.path.join(full_path, version_dir)
                        if os.path.isdir(version_path):
                            version = int(version_dir)
                            config_path = os.path.join(version_path, "model.json")
                            with open(config_path, 'r') as jsonfile:
                                config = json.load(jsonfile)
                                if 'network' in config:
                                    config['network'] = os.path.abspath(os.path.join(version_path, config['network']))
                                if 'weights' in config:
                                    config['weights'] = os.path.abspath(os.path.join(version_path, config['weights']))
                                if 'proc' in config:
                                    config['proc'] = os.path.abspath(os.path.join(version_path, config['proc']))
                                if 'gallery' in config:
                                    config['gallery'] = os.path.abspath(os.path.join(version_path, config['gallery']))
                                if 'labels' in config:
                                    config['labels'] = os.path.abspath(os.path.join(version_path, config['labels']))
                                if 'features' in config:
                                    config['features'] = os.path.abspath(os.path.join(version_path, config['features']))
                                if 'outputs' in config:
                                    for key in config['outputs']:
                                        if 'labels' in config['outputs'][key]:
                                            config['outputs'][key]['labels'] = os.path.abspath(
                                                os.path.join(version_path, config['outputs'][key]['labels']))

            except Exception as error:
                ModelManager.logger.error("Error in Model Loading: {err}".format(err=error))
                model = None

            if model:
                models[model] = {}
                models[model][version] = config

        ModelManager.models = models
        ModelManager.logger.info("Completed Loading Models")

    @staticmethod
    def get_model_parameters(name, version):

        params_obj = {
            "name": name,
            "version": version,
            "type": ModelManager.models[name][version]["type"]
        }

        if "description" in ModelManager.models[name][version]:
            params_obj["description"] = ModelManager.models[name][version]
        return params_obj

    @staticmethod
    def get_loaded_models():
        result = []
        if ModelManager.models is not None:
            for model in ModelManager.models:
                for version in ModelManager.models[model].keys():
                    result.append(ModelManager.get_model_parameters(model, version))

        return result

