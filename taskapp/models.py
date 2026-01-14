from django.db import models
from authapp.models import User

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = (
       ('Pending', 'Pending'),
       ('In Progress', 'In Progress'),
       ('Completed', 'Completed'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    worked_hours = models.PositiveIntegerField(null=True, blank=True)
    completion_report = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)