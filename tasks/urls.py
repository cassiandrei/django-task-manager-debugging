from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("create/", views.create_task, name="create_task"),
    path("complete/<int:task_id>/", views.complete_task, name="complete_task"),
    path("api/overdue/", views.get_overdue_tasks, name="get_overdue_tasks"),
    path("api/by-priority/", views.get_tasks_by_priority, name="get_tasks_by_priority"),
]
