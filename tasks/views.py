from typing import Any

from django.db.models import Case, Count, IntegerField, Prefetch, Q, Value, When
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView,
)

from .forms import TaskForm, TaskListForm
from .models import Task, TaskList


class TaskListCreateView(LoginRequiredMixin, CreateView):
    model = TaskList
    form_class = TaskListForm
    template_name = "tasks/list_form.html"

    def form_valid(self, form):
        # Garante que o usuário logado seja o dono da lista de tarefas criada.
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        assert self.object is not None
        return reverse("tasks:list_detail", kwargs={"pk": self.object.pk})


class TaskListUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskList
    form_class = TaskListForm
    template_name = "tasks/list_form.html"

    def get_queryset(self):
        # Restringe o queryset para objetos pertencentes ao usuário atual.
        return TaskList.objects.filter(user=self.request.user)

    def get_success_url(self):
        assert self.object is not None
        return reverse("tasks:list_detail", kwargs={"pk": self.object.pk})


class TaskListDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskList
    template_name = "tasks/list_confirm_delete.html"
    success_url = "/"

    def get_queryset(self):
        return TaskList.objects.filter(user=self.request.user)


class TaskListDetailView(LoginRequiredMixin, DetailView):
    model = TaskList
    template_name = "tasks/list_detail.html"
    context_object_name = "task_list"  # Usamos `task_list` no template para acessar o objeto da lista de tarefas.

    def get_queryset(self):
        return TaskList.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tasks"] = (
            self.object.tasks.select_related("task_list")
            .annotate(
                status_rank=Case(
                    When(status=Task.Status.PENDING, then=Value(0)),
                    When(status=Task.Status.IN_PROGRESS, then=Value(1)),
                    When(status=Task.Status.DONE, then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            )
            .order_by("status_rank", "due_date", "planned_date", "title")
        )
        ctx["task_count"] = self.object.tasks.count()
        return ctx


class TaskListListView(LoginRequiredMixin, ListView):
    model = TaskList
    template_name = "tasks/list_list.html"
    context_object_name = "task_lists"

    def get_queryset(self):
        task_preview_queryset = Task.objects.order_by(
            "due_date", "planned_date", "title"
        )
        return (
            TaskList.objects.filter(user=self.request.user)
            .annotate(
                task_count=Count("tasks"),
                pending_count=Count(
                    "tasks",
                    filter=Q(
                        tasks__status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]
                    ),
                ),
            )
            .prefetch_related(
                Prefetch(
                    "tasks", queryset=task_preview_queryset, to_attr="preview_tasks"
                )
            )
            .order_by("name")
        )


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_task_list(self) -> TaskList:
        return get_object_or_404(
            TaskList, pk=self.kwargs["list_pk"], user=self.request.user
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["task_list"] = self.get_task_list()
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["task_list"] = self.get_task_list()
        return ctx

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        assert self.object is not None
        return reverse(
            "tasks:task_detail",
            kwargs={"list_pk": self.object.task_list_id, "pk": self.object.pk},
        )


class TaskDetailQuerysetMixin(LoginRequiredMixin):
    request: Any
    kwargs: dict[str, Any]

    def get_queryset(self):
        return Task.objects.filter(
            task_list__user=self.request.user,
            task_list_id=self.kwargs["list_pk"],
        ).select_related("task_list", "owner")


class TaskDetailView(TaskDetailQuerysetMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskUpdateView(TaskDetailQuerysetMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["task_list"] = self.object.task_list
        return ctx

    def get_success_url(self):
        assert self.object is not None
        return reverse(
            "tasks:task_detail",
            kwargs={"list_pk": self.object.task_list_id, "pk": self.object.pk},
        )


class TaskDeleteView(TaskDetailQuerysetMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_success_url(self):
        assert self.object is not None
        return reverse("tasks:list_detail", kwargs={"pk": self.object.task_list_id})


class TaskMarkDoneView(TaskDetailQuerysetMixin, SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.status != Task.Status.DONE:
            task.status = Task.Status.DONE
            task.save(update_fields=["status", "updated_at"])

        next_url = request.headers.get("referer")
        if next_url:
            return redirect(next_url)
        return redirect(
            "tasks:task_detail",
            list_pk=task.task_list_id,
            pk=task.pk,
        )
