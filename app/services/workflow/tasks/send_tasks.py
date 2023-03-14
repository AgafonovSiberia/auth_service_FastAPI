from app.services.workflow.celery import celery


@celery.task
def send_message_with_code(subject: str, address_to: str, code: int):
    pass

