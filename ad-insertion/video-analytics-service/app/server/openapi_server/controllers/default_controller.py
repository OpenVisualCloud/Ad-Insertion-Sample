import connexion
import six

from modules.PipelineManager import PipelineManager
from http import HTTPStatus 
from common.utils import logging
logger = logging.get_logger('Default Controller', is_static=True)

from modules.ModelManager import ModelManager

def models_get():  # noqa: E501
    """models_get

    Return supported models # noqa: E501


    :rtype: List[ModelVersion]
    """
    logger.debug("GET on /models")
    return ModelManager.get_loaded_models()


def pipelines_get():  # noqa: E501
    """pipelines_get

    Return supported pipelines # noqa: E501


    :rtype: List[Pipeline]
    """

    logger.debug("GET on /pipelines")
    return PipelineManager.get_loaded_pipelines()


def pipelines_name_version_get(name, version):  # noqa: E501
    """pipelines_name_version_get

    Return pipeline description and parameters # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: str

    :rtype: None
    """

    logger.debug("GET on /pipelines/{name}/{version}".format(name=name, version=version))
    return PipelineManager.get_pipeline_parameters(name, version)


def pipelines_name_version_instance_id_delete(name, version, instance_id):  # noqa: E501
    """pipelines_name_version_instance_id_delete

    Stop and remove an instance of the customized pipeline # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param instance_id: 
    :type instance_id: int

    :rtype: None
    """

    logger.debug("DELETE on /pipelines/{name}/{version}/{id}".format(name=name, version=version, id=instance_id))
    return PipelineManager.stop_instance(instance_id)


def pipelines_name_version_instance_id_get(name, version, instance_id):  # noqa: E501
    """pipelines_name_version_instance_id_get

    Return instance summary # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param instance_id: 
    :type instance_id: int

    :rtype: object
    """

    logger.debug("GET on /pipelines/{name}/{version}/{id}".format(name=name, version=version, id=instance_id))
    return PipelineManager.get_instance_parameters(instance_id)


def pipelines_name_version_instance_id_status_get(name, version, instance_id):  # noqa: E501
    """pipelines_name_version_instance_id_status_get

    Return instance status summary # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param instance_id: 
    :type instance_id: int

    :rtype: object
    """

    logger.debug("GET on /pipelines/{name}/{version}/{id}/status".format(name=name, version=version, id=instance_id))
    return PipelineManager.get_instance_status(instance_id)


def pipelines_name_version_post(name, version):  # noqa: E501
    """pipelines_name_version_post

    Start new instance of pipeline. Specify the source and destination parameters as URIs # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param pipeline_request: 
    :type pipeline_request: dict | bytes

    :rtype: None
    """

    logger.debug("POST on /pipelines/{name}/{version}".format(name=name, version=version))
    if connexion.request.is_json:
        pipeline_id = PipelineManager.create_instance(name, version, connexion.request.get_json())
        if pipeline_id is not None:
            return pipeline_id

        return ('Invalid Pipeline or Version', HTTPStatus.BAD_REQUEST)
