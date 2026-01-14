
from django.urls import path,include
from authapp import views

urlpatterns = [
    path('',views.login_view,name="loggingin"),
    path('superadmin_dashboard/', views.superadmin_dashboard, name ='superadmin_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name ='admin_dashboard'),
    
    path('admins/', views.admin_list, name='admin_list'),
    path('admins/add/', views.admin_add_edit, name='admin_add'),
    path('admins/edit/<int:id>/', views.admin_add_edit, name='admin_edit'),
    path('admins/toggle-status/<int:id>/', views.toggle_admin_status, name='toggle_admin_status'),


    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add_edit, name='user_add'),
    path('users/edit/<int:id>/', views.user_add_edit, name='user_edit'),
    path('users/delete/<int:id>/', views.user_delete, name='user_delete'),
    
    path('superadmin/assign-user/', views.assign_user_to_admin, name ='assign_user_to_admin'),
    
    path('task/',include('taskapp.urls')),
    path('api/',include('apiapp.urls'))
]
