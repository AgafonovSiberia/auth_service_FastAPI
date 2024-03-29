import asyncio
from abc import ABC
from functools import wraps

from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.db.factory import create_pool


class DatabaseTask(Task, ABC):
    _Session: async_sessionmaker[AsyncSession] = None

    @property
    def session(self) -> async_sessionmaker:
        if self._Session is None:
            self._Session = create_pool()
        return self._Session


def asyncio_celery_task_runner(celery_task):
    @wraps(celery_task)
    def async_wrapper(*args, **kwargs):
        result = asyncio.run(celery_task(*args, **kwargs))
        return result

    return async_wrapper
