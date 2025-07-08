# backend/achilometre/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import todo_views, chess_room_views, weather_views, \
                   home_views, pomodoro_views, profile_views


urlpatterns = [
     path('admin/',
          admin.site.urls),
     # login
     path('login/',
          auth_views.LoginView.as_view(template_name='auth/login.html'),
          name='login'),
     path('logout/',
          todo_views.custom_logout,
          name='logout'),
     # homeview
     path('', home_views.HomeView.as_view(), name='home'),
     # todos
     path("api/add-task/",
          todo_views.add_task_api,
          name="add_task_api"),
     path('task_list/',
          todo_views.TaskListView.as_view(),
          name='task_list'),
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
     # weather
     path('meteo/',
          weather_views.WeatherView.as_view(),
          name='weather'),
     # pomodoro
     path('pomodoro/',
          pomodoro_views.PomodoroView.as_view(),
          name='pomodoro'),
     # profil
     path('profile/',
          profile_views.profile_view,
          name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
