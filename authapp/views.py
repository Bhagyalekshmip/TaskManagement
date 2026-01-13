from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'login.html')

def dashboard(request):
    return render(request,'superuser_dashboard.html')

def list_admin(request):
    return render(request,'admin_list.html')

def list_user(request):
    return render(request,'user_list.html')

def create(request):
    return render(request,'create_form.html')

def edit(request):
    return render(request,'create_form.html')

def asign_usertoadmin(request):
    return render(request,'assign_user_to_admin.html')



