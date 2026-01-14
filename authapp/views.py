from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from authapp.models import User
from .forms import AdminForm, UserForm

# ----------------------------------VIEW FOR LOGIN OF ADMIN/SUPERADMIN/USER---------------------------
def login_view(request):
    error = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Role-based redirection
            if user.role == 'superadmin':
                return redirect('superadmin_dashboard')
            elif user.role == 'admin':
                return redirect('user_list')
            elif user.role == 'user':
                 error = "No UserInterface"
        else:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})

# -------------------------------------------------Dashboard---------------------------------------------

def dashboard(request):
    return render(request,'superuser_dashboard.html')


# -------------------------------------------------admin listing-------------------------------------------------------
def admin_list(request):
    admins = User.objects.filter(role='admin')
    return render(request,'admin_list.html',{'admins': admins})

# ---------------------------------------------------adding and editing admins-----------------------------------------------------
def admin_add_edit(request, id=None):
    admin_obj = None
    if id:
        admin_obj = get_object_or_404(User, id=id, role='admin')

    form = AdminForm(request.POST or None, instance=admin_obj)

    if request.method == 'POST' and form.is_valid():
        admin = form.save(commit=False)
        # IMPORTANT: prevent blank password overwrite
        if not form.cleaned_data.get('password'):
            if admin_obj:
                admin.password = admin_obj.password
                
        admin.role = 'admin'

        password = form.cleaned_data.get('password')
        if password:
            admin.set_password(password)

        admin.save()
        return redirect('admin_list')

    return render(request, 'admin_form.html', {'form': form, 'is_edit': id})

# ------------------------------------disabling admins------------------------------------------------
def toggle_admin_status(request, id):
    admin = get_object_or_404(User, id=id, role='admin')

    if admin.status == 'enable':
        admin.status = 'disable'
    else:
        admin.status = 'enable'

    admin.save()
    return redirect('admin_list')

# ---------------------------------user listing-----------------------------
def user_list(request):
    users = User.objects.filter(role='user')
    return render(request,'user_list.html',{'users':users})

# --------------------------------------------add / edit users-----------------
def user_add_edit(request, id=None):
    user_obj = None
    if id:
        user_obj = get_object_or_404(User, id=id, role='user')

    form = UserForm(request.POST or None, instance=user_obj)
    form.fields['assigned_admin'].queryset = User.objects.filter(role='admin', status='enable')


    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'user'

        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)

        user.save()
        return redirect('user_list')

    return render(request, 'user_form.html', {'form': form, 'is_edit': id})

# ----------------------------deleting the user-------------------------------
def user_delete(request, id):
    user = get_object_or_404(User, id=id, role='user')
    user.delete()
    return redirect('user_list')

# -----------------------------------asigning users to admin-------------------------
def assign_user_to_admin(request):
    admins = User.objects.filter(role='admin')
    users = User.objects.filter(role='user')

    message = None

    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        user_id = request.POST.get('user_id')

        admin = get_object_or_404(User, id=admin_id, role='admin')
        user = get_object_or_404(User, id=user_id, role='user')

        # assign user to admin
        user.assigned_admin = admin
        user.save()

        message = f"{user.username} assigned to {admin.username}"

    return render(request, 'assign_user_to_admin.html', {
        'admins': admins,
        'users': users,
        'message': message
    })


