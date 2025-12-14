import re
from rest_framework.exceptions import ValidationError


class YouTubeLinkValidator:
    def __init__(self, message=None):
        self.message = message or (
            'Разрешены только ссылки на YouTube (youtube.com или youtu.be). '
            'Пример: https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )

    def __call__(self, value):
        # Пропускаем пустые значения
        if not value or not str(value).strip():
            return

        # Проверяем тип
        if not isinstance(value, str):
            raise ValidationError('Значение должно быть строкой.')

        # Регулярное выражение для YouTube
        pattern = re.compile(
            r'^(https?://)?'  # http:// или https://
            r'(www\.)?'  # www.
            r'(youtube\.com|youtu\.be)'  # Домены
            r'(/watch\?v=|/embed/|/)'  # Пути
            r'([\w-]{11})'  # ID видео (11 символов)
            r'(\S*)?$'  # Дополнительные параметры
        )

        if not pattern.match(value.strip()):
            raise ValidationError(self.message)

    def __repr__(self):
        return f'{self.__class__.__name__}(message={self.message})'
