from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
    )
    list_filter = ("name",)
    search_fields = (
        "id",
        "name",
    )

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "course",
    )
    list_filter = ("name",)
    search_fields = (
        "id",
        "name",
        "course",
    )