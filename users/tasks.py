from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более 30 дней
    """
    # Дата, раньше которой last_login считается неактивным
    cutoff_date = timezone.now() - timedelta(days=30)

    # Выбираем пользователей с last_login до cutoff_date и активных (is_active=True)
    inactive_users = User.objects.filter(
        last_login__lt=cutoff_date,
        is_active=True
    )

    # Блокируем
    inactive_users.update(is_active=False)
    # print(f"Заблокировано пользователей: {inactive_users.count()}")
