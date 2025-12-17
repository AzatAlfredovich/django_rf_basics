from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):

    # Способы оплаты
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счёт"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, совершивший платёж",
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты",
        help_text="Дата и время совершения платежа",
    )

    course = models.ForeignKey(
        "materials.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        help_text="Курс, за который произведена оплата",
    )

    lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        help_text="Урок, за который произведена оплата",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Сумма платежа в рублях",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
        help_text="Способ совершения платежа",
    )
    payment_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Ссылка на оплату",
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платёж за курс или урок от {self.user} на {self.amount} руб."


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, подписанный на обновления курса",
        related_name="subscriptions",
    )

    course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Курс, на обновления которого подписался пользователь",
        related_name="subscribers",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата подписки",
        help_text="Когда пользователь подписался на курс",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность подписки",
        help_text="Активна ли подписка (можно отключать без удаления)",
    )

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"
        unique_together = ("user", "course")

    def __str__(self):
        return f"Подписка {self.user} на курс {self.course}"
