from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="example@mail.ru")
        self.course = Course.objects.create(name="Тестовый курс")
        self.lesson = Lesson.objects.create(
            name="Тестовый урок", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "name": "Тестовый урок",
            "description": "Тестовое описание",
            "course": self.course.id,
            "owner": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "Тестовый урок 2",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Тестовый урок 2")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)

        # 1. Проверяем статус
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Проверяем пагинацию
        self.assertEqual(response.data["count"], 1)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

        # 3. Проверяем содержимое урока
        lesson = response.data["results"][0]
        self.assertEqual(lesson["name"], "Тестовый урок")
        self.assertEqual(lesson["course"], self.course.id)
        self.assertEqual(lesson["owner"], self.user.id)
        self.assertIsNone(lesson["image"])
        self.assertIsNone(lesson["video"])


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="example@mail.ru")
        self.course = Course.objects.create(name="Тестовый курс", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Тестовый урок", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "name": "Тестовый курс",
            "description": "Тестовое описание курса",
            "owner": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    @patch("materials.tasks.send_course_update_notification.delay")
    def test_course_update(self, mock_delay):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Тестовый курс 2",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Тестовый курс 2")

        # Проверка, что задача Celery была вызвана (но не выполнялась)
        mock_delay.assert_called_once_with(course_id=self.course.pk)

        # Дополнительно: проверить сохранение в БД
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Тестовый курс 2")

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)

        # 1. Проверяем статус
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Проверяем пагинацию
        self.assertEqual(response.data["count"], 1)
        self.assertIsNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

        # 3. Проверяем содержимое курса
        course = response.data["results"][0]
        self.assertEqual(course["name"], "Тестовый курс")
        self.assertEqual(course["owner"], self.user.id)
