from django.db import models
from django.contrib.auth.models import User


class TaskList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_lists') # related_name funciona como um nome de atributo para acessar as listas de tarefas pelo usuário
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#FFFFFF")  # Default = Branco
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
