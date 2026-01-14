from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    role = models.CharField(max_length=25,choices = ROLE_CHOICES,default='superadmin')
    assigned_admin = models.ForeignKey('self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'},
        related_name='assigned_users')
    
   
    def __str__(self):
        return self.username
