# backend/achilometre/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import todo_views, chess_room_views


urlpatterns = [
    path('admin/',
         admin.site.urls),
    path('',
         todo_views.TaskListView.as_view(),
         name='task_list'),
    # login
    path('login/',
         auth_views.LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('logout/',
         todo_views.custom_logout,
         name='logout'),
    # todos
    path('add/',
         todo_views.TaskCreateView.as_view(),
         name='task_add'),
    path('edit/<int:pk>/',
         todo_views.TaskUpdateView.as_view(),
         name='task_edit'),
    path('delete/<int:pk>/',
         todo_views.TaskDeleteView.as_view(),
         name='task_delete'),
    path('task/<int:pk>/toggle/',
         todo_views.toggle_task_status,
         name='toggle_task'),
    # chessroom
    path('chess_room/',
         chess_room_views.ChessRoomView.as_view(),
         name='chess_room'),
]
