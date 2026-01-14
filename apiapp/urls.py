from django.urls import path
from apiapp import views

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('tasks/', views.user_tasks, name='user_tasks'),
    path('tasks/<int:id>/', views.update_task_status, name='update_task_status'),
    path('tasks/<int:id>/report/', views.task_completion_report, name='task_completion_report'),
]
