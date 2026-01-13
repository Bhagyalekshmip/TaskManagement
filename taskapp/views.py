from django.shortcuts import render

def all_tasks(request):
    return render(request,'all_tasks.html')

def list_task_reports(request):
    return render(request,'list_task_reports.html')

def task_reports(request):
    return render(request,'task_reports.html')

def asign_tasktouser(request):
    return render(request,'assign_tasktouser.html')

def admin_task_list(request):
    return render(request, 'admin_task_list.html')

def admin_task_report(request):
    return render(request, 'task_reports.html')

def delete_task(request):
    return render(request, 'admin_task_list.html')