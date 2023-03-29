from celery import Celery
from app.config_reader import config


celery = Celery("web",
                broker=config.REDIS_URL,
                backend=config.REDIS_URL,
                include=["app.infrastructure.workflow.tasks.send_tasks",
                         "app.infrastructure.workflow.tasks.periodic"])


class CeleryConfig:
    timezone = "Europe/Moscow"


celery.config_from_object(CeleryConfig)