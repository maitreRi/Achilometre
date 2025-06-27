# backend/achilometre/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin/',
         admin.site.urls),
    path('',
         views.TaskListView.as_view(),
         name='task_list'),
    path('add/',
         views.TaskCreateView.as_view(),
         name='task_add'),
    path('edit/<int:pk>/',
         views.TaskUpdateView.as_view(),
         name='task_edit'),
    path('delete/<int:pk>/',
         views.TaskDeleteView.as_view(),
         name='task_delete'),
    path('login/',
         auth_views.LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('logout/',
         views.custom_logout,
         name='logout'),
]
