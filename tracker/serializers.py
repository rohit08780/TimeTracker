# tasks/serializers.py

from rest_framework import serializers
from .models import Task, User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'hours_spent', 'date', 'status', 'employee', 'manager_comment']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']


