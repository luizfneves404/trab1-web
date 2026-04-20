from django.urls import path
from .views import (
    TaskListCreateView, TaskListUpdateView,
    TaskListDeleteView, TaskListDetailView,
)

# app_name funciona como um namespace para as URLs do app tasks, permitindo que sejam referenciadas de forma única em todo o projeto, mesmo que outros apps tenham URLs com os mesmos nomes.
app_name = 'tasks'

urlpatterns = [
    path('lists/new/', TaskListCreateView.as_view(), name='list_create'), # Usamos name para referenciar a URL em templates e views.
    path('lists/<int:pk>/edit/', TaskListUpdateView.as_view(), name='list_update'),
    path('lists/<int:pk>/delete/', TaskListDeleteView.as_view(), name='list_delete'),
    path('lists/<int:pk>/', TaskListDetailView.as_view(), name='list_detail'),
]
