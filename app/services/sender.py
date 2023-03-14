from abc import ABC, abstractmethod
from redmail import EmailSender
from app.config_reader import config


class CodeSender(ABC):
    message_to: str = None

    @abstractmethod
    def send_message(self, message: EmailSender | str):
        raise NotImplementedError


class SMSCodeSender(CodeSender):
    def send_message(self, message):
        pass


class EmailCodeSender:
    def __init__(self):
        self.email = EmailSender(host=config.EMAIL.HOST,
                                 port=config.EMAIL.PORT,
                                 use_tls=config.EMAIL.USE_TLS,
                                 username=config.EMAIL.LOGIN,
                                 password=config.EMAIL.PASSWORD)

    def send_email(self,
                   subject: str,
                   email_to: str,
                   html_template_name: str,
                   body_params: dict[str, str]):

        self._set_template()
        self.email.send(
            subject=subject,
            receivers=[email_to],
            html_template=html_template_name,
            body_params=body_params
        )

    def _set_template(self):
        self.email.set_template_paths(config.EMAIL.TEMPLATE_PATH)

