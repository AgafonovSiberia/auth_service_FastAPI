from celery.app import task
from celery.schedules import crontab

from app.infrastructure.repo.base import SQLALchemyRepo
from app.infrastructure.repo.user_repo import UserRepo
from app.infrastructure.workflow.utils import DatabaseTask, asyncio_celery_task_runner
from app.infrastructure.workflow.worker import celery


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    """
    Определяет периодические задачи для celery beat
    """
    sender.add_periodic_task(
        crontab(hour=9, minute=0),
        clean_expire_code_activate.s(),
        name="delete_expire_activate_codes",
    )


@celery.task(base=DatabaseTask, bind=True)
@asyncio_celery_task_runner
async def clean_expire_code_activate(self: task) -> None:
    async with self.session() as _session:
        repo = SQLALchemyRepo(_session)
        await repo.get_repo(UserRepo).delete_expire_activate_codes()
