class AppException(Exception):
    msg = "⚠️ Неизвестная ошибка"

    def __str__(self) -> str:
        return self.msg