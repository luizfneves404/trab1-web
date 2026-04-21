from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from .models import TaskList
from .forms import TaskListForm


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
        # Envia as tarefas da lista para o template.
        ctx["tasks"] = (
            self.object.tasks.all()
        )  # Funciona por conta de related_name='tasks' na ForeignKey de Task para TaskList.
        return ctx
