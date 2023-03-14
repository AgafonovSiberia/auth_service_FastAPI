from abc import ABC, abstractmethod
from redmail import EmailSender
from app.config_reader import config
import re

from email_validator import validate_email, EmailNotValidError

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


class CodeSender:
    def __init__(self, subject: str, address_to: str,code: int):
        self.subject = subject
        self.address_to = address_to
        self.code = code

    def send(self):
        if self._is_email(self.address_to):
            sender = EmailCodeSender()
            sender.send_email(email_to=self.address_to,
                              **self._get_data_to_email(),
                              body_params={"login": self.address_to, "code": self.code})

        if self._is_phone_number(self.address_to):
            pass

    def _get_data_to_email(self):
        mail_subject, template = ("Ваш аккаунт активирован", "activate.html")\
            if self.subject == "activate" else ("Восстановление пароля", "password_reset.html")
        return {"subject": mail_subject, "html_template_name": template}

    def _is_phone_number(self):
        some_string = self.address_to.strip().replace(' ', '')
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if some_string and not re.search(regex, some_string, re.I):
            return False
        return True

    def _is_email(self):
        try:
            validate_email(self.address_to)
        except EmailNotValidError:
            return False
        else:
            return True




