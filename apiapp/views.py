from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from taskapp.models import Task
from .serializers import TaskSerializer
# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'username': user.username,
        'role': user.role
    })
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def user_tasks(request):
    """
    GET /tasks
    Returns all tasks assigned to the logged-in user
    """
    user = request.user
    tasks = Task.objects.filter(assigned_to=user).order_by('-due_date')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_status(request, id):
    user = request.user
    try:
        task = Task.objects.get(id=id, assigned_to=user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found or not assigned to you'},
                        status=status.HTTP_404_NOT_FOUND)
        
    status_value = request.data.get('status')
    completion_report = request.data.get('completion_report')
    worked_hours = request.data.get('worked_hours')
    
    if status_value == 'Completed':
        if not completion_report or not worked_hours:
            return Response(
                {'error': 'completion_report and worked_hours are required when completing a task'},
                status=status.HTTP_400_BAD_REQUEST
            )
        task.status = 'Completed'
        task.completion_report = completion_report
        task.worked_hours = worked_hours
        task.save()
    
    elif status_value in ['Pending', 'In Progress']:
        task.status = status_value
        task.save()
    
    else:
        return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Return the task in all cases
    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_completion_report(request, id):
    
    user = request.user

    # Check role
    if user.role not in ['admin', 'superadmin']:
        return Response({'error': 'You do not have permission to view this report'},
                        status=status.HTTP_403_FORBIDDEN)

    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if task.status != 'Completed':
        return Response({'error': 'Task is not completed yet'}, status=status.HTTP_400_BAD_REQUEST)

     # Admin can only view tasks of their assigned users
    if user.role == 'admin':
        if task.assigned_to.assigned_admin != user:
            return Response({'error': 'You do not have permission to view this report'},
                            status=status.HTTP_403_FORBIDDEN)
            
    # Return only completion report and worked hours
    data = {
        'id': task.id,
        'title': task.title,
        'assigned_to': task.assigned_to.username,
        'created_by': task.created_by.username,
        'completion_report': task.completion_report,
        'worked_hours': task.worked_hours
    }
    return Response(data)