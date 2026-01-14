from django.urls import path
from taskapp import views

urlpatterns = [
    path('all_tasks/', views.all_tasks, name ='all_tasks'),
    path('task_reports/<int:id>/', views.task_reports, name='task_reports'),
    path('list_completedtask/', views.list_completedtask, name ='list_completedtask'),
    # ------------------admis---------------
    # urls.py
   path('admin/assigned-users/', views.assigned_users_list, name='assigned_users_list'),

    path('tasktouser/', views.asign_tasktouser, name ='asign_tasktouser'),
    path('admin/tasks/', views.admin_task_list, name='admin_task_list'),
    path('admin/tasks/report/', views.admin_task_report, name='admin_task_report'),
    path('admin/tasks/delete/', views.delete_task, name='delete_task'),
]