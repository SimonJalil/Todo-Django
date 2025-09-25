"""
URL configuration for todo_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from tasks import views 
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks_completed/", views.tasks_completed, name="tasks_completed"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.signin, name="signin"),
    path("create-task/", views.create_task, name="create_task"),
    path("task/<int:task_id>/", views.task_detail, name="task_detail"),
    path("task/<int:task_id>/complete/", views.complete_task, name="complete_task"),
    path("task/<int:task_id>/delete/", views.delete_task, name="delete_task"),
]

# URLs para probar páginas de error (solo en desarrollo)
if settings.DEBUG:
    urlpatterns += [
        path('404-test/', lambda request: render(request, '404.html')),
        path('500-test/', lambda request: render(request, '500.html')),
        path('403-test/', lambda request: render(request, '403.html')),
    ]

# HANDLERS DE ERROR (DEBEN ESTAR AL FINAL DEL ARCHIVO)
handler404 = 'tasks.views.custom_404'  # Asegúrate de que 'tasks' sea el nombre correcto de tu app
handler500 = 'tasks.views.custom_500'
handler403 = 'tasks.views.custom_403'