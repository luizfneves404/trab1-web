from django.urls import path
from .views import (
    SubTaskCreateView,
    SubTaskDeleteView,
    SubTaskToggleView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListCreateView,
    TaskMarkDoneView,
    TaskUpdateView,
    TaskListUpdateView,
    TaskListDeleteView,
    TaskListDetailView,
    TaskListListView,
)

# app_name funciona como um namespace para as URLs do app tasks, permitindo que sejam referenciadas de forma única em todo o projeto, mesmo que outros apps tenham URLs com os mesmos nomes.
app_name = "tasks"

urlpatterns = [
    # A lista de tarefas é a navegação principal do app; as rotas de task partem dela.
    path("lists/", TaskListListView.as_view(), name="list_list"),
    path(
        "lists/new/", TaskListCreateView.as_view(), name="list_create"
    ),  # Usamos name para referenciar a URL em templates e views.
    path("lists/<int:pk>/edit/", TaskListUpdateView.as_view(), name="list_update"),
    path("lists/<int:pk>/delete/", TaskListDeleteView.as_view(), name="list_delete"),
    path("lists/<int:pk>/", TaskListDetailView.as_view(), name="list_detail"),
    # As tasks sempre vivem dentro de uma lista, por isso list_pk na URL.
    path(
        "lists/<int:list_pk>/tasks/new/",
        TaskCreateView.as_view(),
        name="task_create",
    ),
    path(
        "lists/<int:list_pk>/tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task_detail",
    ),
    path(
        "lists/<int:list_pk>/tasks/<int:pk>/edit/",
        TaskUpdateView.as_view(),
        name="task_update",
    ),
    path(
        "lists/<int:list_pk>/tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task_delete",
    ),
    path(
        "lists/<int:list_pk>/tasks/<int:pk>/done/",
        TaskMarkDoneView.as_view(),
        name="task_mark_done",
    ),
    # Subtasks são aninhadas abaixo da task pai.
    path(
        "lists/<int:list_pk>/tasks/<int:pk>/subtasks/new/",
        SubTaskCreateView.as_view(),
        name="subtask_create",
    ),
    path(
        "lists/<int:list_pk>/tasks/<int:pk>/subtasks/<int:subtask_pk>/toggle/",
        SubTaskToggleView.as_view(),
        name="subtask_toggle",
    ),
    path(
        "lists/<int:list_pk>/tasks/<int:pk>/subtasks/<int:subtask_pk>/delete/",
        SubTaskDeleteView.as_view(),
        name="subtask_delete",
    ),
]
