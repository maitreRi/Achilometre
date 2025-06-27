from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('add/', views.TaskCreateView.as_view(), name='task_add'),
    path('edit/<int:pk>/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task_delete'),
]
