from django import forms
from .models import SubTask, Task, TaskList


def style_fields(fields):
    for field in fields.values():
        widget = field.widget
        if isinstance(widget, forms.Select):
            widget.attrs.setdefault("class", "select select-bordered w-full")
        elif isinstance(widget, forms.Textarea):
            widget.attrs.setdefault("class", "textarea textarea-bordered w-full")
        elif isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", "checkbox")
        elif widget.input_type == "color":
            widget.attrs.setdefault("class", "input input-bordered h-12 w-full")
        else:
            widget.attrs.setdefault("class", "input input-bordered w-full")


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ["name", "description", "color"]  # O campo user é definido na view.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_fields(self.fields)


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
            # Usamos o seletor nativo de data do navegador.
            "due_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "planned_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        style_fields(self.fields)
        if user is not None:
            # Evita que o usuário mova tasks para listas de terceiros.
            self.fields["task_list"].queryset = TaskList.objects.filter(
                user=user
            ).order_by("name")


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_fields(self.fields)
