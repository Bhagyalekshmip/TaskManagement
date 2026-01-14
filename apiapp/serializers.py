from rest_framework import serializers
from taskapp.models import Task

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'created_by', 'assigned_to', 'completion_report', 'worked_hours']
        read_only_fields = ['assigned_by', 'assigned_to']
