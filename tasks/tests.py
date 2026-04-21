from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Task, TaskList


class TaskListDetailViewTests(TestCase):
    def test_owner_can_open_list_detail_with_tasks(self) -> None:
        user = User.objects.create_user("owner", "owner@example.com", "sE7!kM2@nP9#xQ1")
        task_list = TaskList.objects.create(user=user, name="Compras")
        Task.objects.create(task_list=task_list, title="Leite", done=False)
        self.client.force_login(user)

        response = self.client.get(
            reverse("tasks:list_detail", kwargs={"pk": task_list.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compras")
        self.assertContains(response, "Leite")
