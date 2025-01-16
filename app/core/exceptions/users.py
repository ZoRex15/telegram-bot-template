from app.core.exceptions.base import AppException


class UsersException(AppException):
    pass

class UserNotFound(UsersException):
    msg = "Пользователь не был найден"
    