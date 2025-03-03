from app.core.exceptions.base import AppException


class MailingsException(AppException):
    pass

class MailingNotFound(MailingsException):
    msg = "Рассылка не был найден"
    