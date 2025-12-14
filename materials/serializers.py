from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    # lessons = SerializerMethodField()

    def get_lessons_count(self, instance):
        return Lesson.objects.filter(course=instance).count()

    # def get_lessons(self, instance):
    #     lessons = Lesson.objects.filter(course = instance)
    #     serializer = LessonSerializer(lessons, many = True)
    #     return serializer.data

    class Meta:
        model = Course
        fields = ("name", "image", "description", "lessons_count", "lessons")
