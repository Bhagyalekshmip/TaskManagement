from django.shortcuts import render,redirect,get_object_or_404
from taskapp.models import Task
from authapp.models import User

def all_tasks(request):
    user = request.user

    # Super Admin → all tasks
    if user.role == 'superadmin':
        tasks = Task.objects.select_related(
            'assigned_to',
            'assigned_to__assigned_admin'
        ).all()

    # Admin → tasks assigned by this admin
    elif user.role == 'admin':
        tasks = Task.objects.select_related(
            'assigned_to',
            'assigned_to__assigned_admin'
        ).filter(created_by=user)

    # User → tasks assigned to this user
    else:
        tasks = Task.objects.filter(assigned_to=user)

    return render(request, 'all_tasks.html', {'tasks': tasks})


def list_completedtask(request):
    user = request.user

    if user.role == 'superadmin':
        # Superadmin sees all completed tasks
        completed_tasks = Task.objects.filter(status='Completed').select_related('assigned_to', 'assigned_to__assigned_admin')
    elif user.role == 'admin':
        # Admin sees only their users' completed tasks
        completed_tasks = Task.objects.filter(
            status='Completed',
            assigned_to__assigned_admin=user
        ).select_related('assigned_to', 'assigned_to__assigned_admin')
    else:
        completed_tasks = []

    return render(request, 'list_completedtask.html', {'completed_tasks': completed_tasks})


from django.http import Http404


def task_reports(request, id):
    user = request.user

    # Get the task or 404
    task = get_object_or_404(Task, id=id)  # only completed tasks

    # Authorization check
    if user.role == 'admin':
        # Admin can only see tasks of users assigned to them
        if task.assigned_to.assigned_admin != user:
            raise Http404("You are not authorized to view this task")
    
    # Superadmin can view all tasks

    return render(request, 'task_reports.html', {'task': task})


def asign_tasktouser(request):
    admin = request.user  # currently logged-in admin



    # Only users assigned to THIS admin
    users = User.objects.filter(role='user', assigned_admin=admin)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')

        assigned_user = User.objects.get(id=user_id)

        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_user,
            created_by=admin,
            due_date=due_date
        )

        return redirect('superadmin_dashboard')

    return render(request, 'assign_tasktouser.html', {'users': users})
    
    
def assigned_users_list(request):
    user = request.user

    if user.role != 'admin':
        # Only admins can access this page
        return render(request, 'superadmin_dashboard.html')  # optional template

    # Get all users assigned to this admin
    assigned_users = User.objects.filter(assigned_admin=user)

    return render(request, 'assigned_users_list.html', {'assigned_users': assigned_users})


def admin_task_list(request):
    return render(request, 'admin_task_list.html')

def admin_task_report(request):
    return render(request, 'task_reports.html')

def delete_task(request):
    return render(request, 'admin_task_list.html')