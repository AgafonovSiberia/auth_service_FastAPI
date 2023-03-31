from celery import Celery
from app.config_reader import config


celery = Celery(
    "web",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL,
    include=[
        "app.infrastructure.workflows.tasks.send_tasks",
        "app.infrastructure.workflows.tasks.periodic",
    ],
)


class CeleryConfig:
    timezone = "Europe/Moscow"


celery.config_from_object(CeleryConfig)
