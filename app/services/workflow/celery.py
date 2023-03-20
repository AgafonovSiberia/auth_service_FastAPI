from celery import Celery
from celery.beat import PersistentScheduler
from app.config_reader import config


celery = Celery("web",
                broker=config.REDIS_URL,
                backend=config.REDIS_URL,
                include=["app.services.workflow.tasks.send_tasks"])


class CeleryConfig:
    timezone = "Europe/Moscow"


celery.config_from_object(CeleryConfig)