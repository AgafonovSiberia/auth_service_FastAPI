from app.infrastructure.workflow.celery import celery
from app.utils.sender import CodeSender


@celery.task
def send_message_with_code(subject: str, address_to: str, code: int):
    sender = CodeSender(subject=subject, address_to=address_to, code=code)
    sender.send()




