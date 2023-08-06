import time
from abc import ABC
from typing import Optional, Dict

from lgt.common.python.lgt_logging import log
from lgt_data.model import BotModel
from lgt_data.mongo_repository import BotMongoRepository, DedicatedBotRepository, UserMongoRepository
from pydantic import BaseModel, conlist

from ..k8client import KubernetesClientFactory, KubernetesAppsClient
from .. import BaseBackgroundJobData, BaseBackgroundJob
from ..env import k8namespace, backend_uri, aggregator_topic, project_id, \
    google_app_credentials

"""
Restart Bots
"""
class RestartDedicatedBotsJobData(BaseBackgroundJobData, BaseModel):
    user_id: str

class RestartDedicatedBotsJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return RestartDedicatedBotsJobData

    def exec(self, data: RestartDedicatedBotsJobData):
        deployment_labels = { "type": "dedicated-slack-bot" }

        client = KubernetesClientFactory.create()
        client.remove_deployments(k8namespace, deployment_labels)
        bots = DedicatedBotRepository().get_user_bots(data.user_id)
        user = UserMongoRepository().get(data.user_id)

        if not bots:
            return

        response = client.create_slack_bots_deployment(namespace=k8namespace,
                                                       name=f"{user.email}-dedicated-bots",
                                                       backend_uri=backend_uri,
                                                       bots=bots,
                                                       project_id=project_id,
                                                       aggregator_topic=aggregator_topic,
                                                       google_app_credentials=google_app_credentials,
                                                       labels=deployment_labels)