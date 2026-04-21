from django.contrib import admin

from .models import Task, TaskList


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    search_fields = ("name", "user__username")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "task_list",
        "owner",
        "status",
        "priority",
        "due_date",
        "planned_date",
    )
    search_fields = ("title", "task_list__name", "owner__username")
