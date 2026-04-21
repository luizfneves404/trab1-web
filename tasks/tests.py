from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import SubTask, Task, TaskList


class TaskListDetailViewTests(TestCase):
    def test_owner_can_open_list_detail_with_tasks(self) -> None:
        user = User.objects.create_user("owner", "owner@example.com", "sE7!kM2@nP9#xQ1")
        task_list = TaskList.objects.create(user=user, name="Compras")
        Task.objects.create(task_list=task_list, title="Leite")
        self.client.force_login(user)

        response = self.client.get(
            reverse("tasks:list_detail", kwargs={"pk": task_list.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compras")
        self.assertContains(response, "Leite")


class TaskCrudViewTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            "owner", "owner@example.com", "sE7!kM2@nP9#xQ1"
        )
        self.other_user = User.objects.create_user(
            "other", "other@example.com", "sE7!kM2@nP9#xQ1"
        )
        self.task_list = TaskList.objects.create(user=self.user, name="Compras")
        self.other_list = TaskList.objects.create(user=self.other_user, name="Trabalho")

    def test_user_can_create_task_within_list(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("tasks:task_create", kwargs={"list_pk": self.task_list.pk}),
            {
                "task_list": self.task_list.pk,
                "title": "Leite",
                "description": "Integral",
                "priority": Task.Priority.HIGH,
                "status": Task.Status.PENDING,
                "due_date": "2026-04-30",
                "planned_date": "2026-04-21",
            },
        )

        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(title="Leite")
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.task_list, self.task_list)

    def test_user_can_mark_task_done(self) -> None:
        task = Task.objects.create(task_list=self.task_list, title="Leite")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "tasks:task_mark_done",
                kwargs={"list_pk": self.task_list.pk, "pk": task.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)

    def test_task_update_form_keeps_existing_dates_visible(self) -> None:
        task = Task.objects.create(
            task_list=self.task_list,
            title="Leite",
            due_date="2026-04-30",
            planned_date="2026-04-21",
        )
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "tasks:task_update",
                kwargs={"list_pk": self.task_list.pk, "pk": task.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="2026-04-30"')
        self.assertContains(response, 'value="2026-04-21"')

    def test_list_view_shows_task_previews_and_empty_state(self) -> None:
        empty_list = TaskList.objects.create(user=self.user, name="Vazia")
        Task.objects.create(
            task_list=self.task_list,
            title="Leite",
            due_date="2026-04-30",
        )
        Task.objects.create(
            task_list=self.task_list,
            title="Pão",
            planned_date="2026-04-21",
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("tasks:list_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leite")
        self.assertContains(response, "Prazo: 30/04/2026")
        self.assertContains(response, "Pão")
        self.assertContains(response, "Prazo: sem prazo")
        self.assertContains(response, "0 tarefas")
        self.assertContains(response, empty_list.name)

    def test_user_cannot_open_other_users_task(self) -> None:
        task = Task.objects.create(task_list=self.other_list, title="Privada")
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "tasks:task_detail",
                kwargs={"list_pk": self.other_list.pk, "pk": task.pk},
            )
        )

        self.assertEqual(response.status_code, 404)


class SubTaskViewTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            "owner", "owner@example.com", "sE7!kM2@nP9#xQ1"
        )
        self.other_user = User.objects.create_user(
            "other", "other@example.com", "sE7!kM2@nP9#xQ1"
        )
        self.task_list = TaskList.objects.create(user=self.user, name="Compras")
        self.task = Task.objects.create(
            owner=self.user,
            task_list=self.task_list,
            title="Mercado",
        )
        self.other_list = TaskList.objects.create(user=self.other_user, name="Trabalho")
        self.other_task = Task.objects.create(
            owner=self.other_user,
            task_list=self.other_list,
            title="Privada",
        )

    def test_owner_can_open_task_detail_with_subtasks(self) -> None:
        SubTask.objects.create(task=self.task, title="Comprar leite")
        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "tasks:task_detail",
                kwargs={"list_pk": self.task_list.pk, "pk": self.task.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subtarefas")
        self.assertContains(response, "Comprar leite")

    def test_owner_can_create_subtask(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "tasks:subtask_create",
                kwargs={"list_pk": self.task_list.pk, "pk": self.task.pk},
            ),
            {"title": "Comprar pão"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            SubTask.objects.filter(task=self.task, title="Comprar pão").exists()
        )

    def test_owner_can_toggle_subtask(self) -> None:
        subtask = SubTask.objects.create(task=self.task, title="Comprar leite")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "tasks:subtask_toggle",
                kwargs={
                    "list_pk": self.task_list.pk,
                    "pk": self.task.pk,
                    "subtask_pk": subtask.pk,
                },
            )
        )

        self.assertEqual(response.status_code, 302)
        subtask.refresh_from_db()
        self.assertTrue(subtask.done)

    def test_owner_can_delete_subtask(self) -> None:
        subtask = SubTask.objects.create(task=self.task, title="Comprar leite")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "tasks:subtask_delete",
                kwargs={
                    "list_pk": self.task_list.pk,
                    "pk": self.task.pk,
                    "subtask_pk": subtask.pk,
                },
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(SubTask.objects.filter(pk=subtask.pk).exists())

    def test_user_cannot_create_subtask_for_other_users_task(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "tasks:subtask_create",
                kwargs={"list_pk": self.other_list.pk, "pk": self.other_task.pk},
            ),
            {"title": "Invadir"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            SubTask.objects.filter(task=self.other_task, title="Invadir").exists()
        )

    def test_user_cannot_toggle_other_users_subtask(self) -> None:
        subtask = SubTask.objects.create(task=self.other_task, title="Privada")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "tasks:subtask_toggle",
                kwargs={
                    "list_pk": self.other_list.pk,
                    "pk": self.other_task.pk,
                    "subtask_pk": subtask.pk,
                },
            )
        )

        self.assertEqual(response.status_code, 404)
        subtask.refresh_from_db()
        self.assertFalse(subtask.done)

    def test_deleting_task_deletes_subtasks(self) -> None:
        SubTask.objects.create(task=self.task, title="Comprar leite")

        self.task.delete()

        self.assertFalse(SubTask.objects.exists())
