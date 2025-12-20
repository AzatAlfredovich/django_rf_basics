from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import YouTubeLinkValidator
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    video = serializers.URLField(
        required=False, allow_blank=True, validators=[YouTubeLinkValidator()]
    )

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "image", "course", "owner", "video"]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, instance):
        return Lesson.objects.filter(course=instance).count()

    def get_is_subscribed(self, instance):
        request = self.context.get("request")
        # Проверяем, есть ли активный запрос и авторизованный пользователь
        if not request or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(
            user=request.user, course=instance, is_active=True
        ).exists()

    class Meta:
        model = Course
        fields = (
            "name",
            "image",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )
