
from django.urls import path,include
from authapp import views

urlpatterns = [
    path('',views.login,name="login"),
    path('dashboard/', views.dashboard, name ='superadmin_dashboard'),
    path('list_admin/', views.list_admin, name ='list_admin'),
    path('list_user/', views.list_user, name ='list_user'),
    path('create/', views.create, name ='create'),
    path('edit/', views.edit, name ='edit'),
    path('usertoadmin/', views.asign_usertoadmin, name ='asign_usertoadmin'),
    path('task/',include('taskapp.urls'))
]
