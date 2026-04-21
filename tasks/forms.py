from django import forms
from .models import TaskList


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ["name", "description", "color"]  # O campo user é definido na view.
