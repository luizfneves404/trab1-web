from django import forms
from .models import Task, TaskList


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ["name", "description", "color"]  # O campo user é definido na view.


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_list",
            "title",
            "description",
            "priority",
            "status",
            "due_date",
            "planned_date",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "planned_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["task_list"].queryset = TaskList.objects.filter(
                user=user
            ).order_by("name")
