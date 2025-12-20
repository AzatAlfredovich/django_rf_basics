from django.urls import reverse
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import Subscription, User


class SubscriptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="example@mail.ru")
        self.course = Course.objects.create(name="Курс")
        self.url = reverse("users:subscriptions")

    def test_subscribe(self):
        """Простая подписка"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url, {"course_id": self.course.id}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(response.data["is_subscribed"])

        # Проверяем, что подписка создана
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe(self):
        """Простая отписка"""
        # Сначала подписываемся
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.url, {"course_id": self.course.id}, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(response.data["is_subscribed"])

        # Проверяем, что подписка удалена
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_no_auth(self):
        """Без авторизации — ошибка"""
        response = self.client.post(
            self.url, {"course_id": self.course.id}, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_no_course_id(self):
        """Без course_id — ошибка"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
