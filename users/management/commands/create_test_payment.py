import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт тестовые платежи, пользователя, курс и уроки, если их нет"

    def handle(self, *args, **options):
        self.stdout.write("Начинаем создание тестовых данных...")

        # 1. Создаём тестового пользователя (id=2), если его нет (id=1 - это админ!)
        test_user, created = User.objects.get_or_create(
            id=2,
            email="testuser@example.com",
            first_name="Тестовый",
            last_name="Пользователь",
        )
        if created:
            test_user.set_password("testpass123")
            test_user.save()
            self.stdout.write(
                self.style.SUCCESS("Создан тестовый пользователь (id=2): testuser")
            )
        else:
            self.stdout.write("Тестовый пользователь (id=2) уже существует")

        # 2. Создаём курс, если нет ни одного
        if not Course.objects.exists():
            course = Course.objects.create(
                name="Базовый курс Python",
                description="Введение в программирование на Python",
            )
            self.stdout.write(self.style.SUCCESS('Создан курс: "Базовый курс Python"'))
        else:
            course = Course.objects.first()  # берём первый существующий

        # 3. Создаём 3 урока для курса, если их мало
        existing_lessons = Lesson.objects.filter(course=course)
        if existing_lessons.count() < 3:
            for i in range(1, 4):
                lesson = Lesson.objects.create(
                    name=f"Урок {i}: Основы",
                    description=f"Содержание урока {i}",
                    course=course,
                )
                self.stdout.write(self.style.SUCCESS(f'Создан урок: "{lesson.name}"'))
        lessons = list(Lesson.objects.filter(course=course)[:3])  # берём первые 3

        # 4. Создаём тестовые платежи
        payments = []
        payment_count = random.randint(3, 5)  # от 3 до 5 платежей

        for i in range(payment_count):
            # Случайная дата за последние 30 дней
            days_ago = random.randint(0, 30)
            payment_date = datetime.now() - timedelta(
                days=days_ago, hours=random.randint(0, 23)
            )

            # Случайная сумма от 500 до 5000 руб.
            amount = round(random.uniform(500, 5000), 2)

            # Случайный способ оплаты
            payment_method = random.choice(["cash", "transfer"])

            # Случайный выбор: платить за курс или за урок
            if random.choice([True, False]):
                course_payment = course
                lesson_payment = None
            else:
                course_payment = None
                lesson_payment = random.choice(lessons)

            payment = Payment(
                user=test_user,
                payment_date=payment_date,
                course=course_payment,
                lesson=lesson_payment,
                amount=amount,
                payment_method=payment_method,
            )
            payments.append(payment)

        # Сохраняем все платежи разом (быстрее)
        Payment.objects.bulk_create(payments)
        self.stdout.write(
            self.style.SUCCESS(f"Создано {len(payments)} тестовых платежей!")
        )

        # 5. Вывод информации
        self.stdout.write("\nСводка:")
        self.stdout.write(f"  Пользователь: {test_user.email} (id={test_user.id})")
        self.stdout.write(f"  Курс: {course.name} (id={course.id})")
        self.stdout.write(f"  Уроки: {[lesson.name for lesson in lessons]}")
        self.stdout.write(f"  Платежи: {len(payments)} записей в таблице Payment")
