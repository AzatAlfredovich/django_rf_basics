from django.db import models, transaction

from users.models import User


# Курс
class Course(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )

    image = models.ImageField(
        upload_to="materials/photo",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение",
    )

    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления",
        help_text="Дата и время последнего изменения курса (включая связанные уроки)",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"Курс '{self.name}'"


# Урок
class Lesson(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )

    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание",
    )

    image = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение",
    )

    video = models.URLField(
        blank=True,
        null=True,
        verbose_name="Видео",
        help_text="Введите ссылку на урок",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"Урок '{self.name}'"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.course is not None:
                self.course.save(update_fields=['updated_at'])

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            course_instance = self.course
            super().delete(*args, **kwargs)
            if course_instance is not None:
                course_instance.save(update_fields=['updated_at'])
