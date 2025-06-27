# backend/achilometre/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from todos.views import custom_logout


urlpatterns = [
    path('admin/', admin.site.urls),

    # # Auth (connexion/déconnexion)
    path('login/',
         auth_views.LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('logout/', custom_logout, name='logout'),



    # App todos
    path('', include('todos.urls')),
]
