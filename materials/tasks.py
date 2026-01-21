from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from materials.models import Course
from users.models import Subscription


@shared_task
def send_course_update_notification(course_id):
    """
    Отправляет уведомление подписчикам об обновлении курса.
    Отправляет только если:
    - прошло ≥4 часов с последнего обновления материалов;
    - есть активные подписчики с email
    """
    course = Course.objects.get(id=course_id)

    # Проверка времени последнего обновления (4 часа)
    if (timezone.now() - course.updated_at) < timedelta(hours=4):
        return  # Слишком рано для отправки

    # Сбор email активных подписчиков
    subscribers = Subscription.objects.filter(course=course, is_active=True)
    emails = [s.user.email for s in subscribers if s.user.email and "@" in s.user.email]

    if not emails:
        return  # Нет адресов для отправки

    # Формирование письма
    subject = f"Обновление: {course.name}"
    message = (
        f"Курс '{course.name}' был обновлён.\n"
        "Ознакомьтесь с новыми материалами в личном кабинете."
    )

    # Отправка
    send_mail(
        subject=subject,
        message=message,
        from_email="notification@yandex.ru",
        recipient_list=emails,
        fail_silently=False,
    )
