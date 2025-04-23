# tasks/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# User model ke liye role-based system
class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

# Task model
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    hours_spent = models.PositiveIntegerField()
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    employee = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    manager_comment = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Validation: Ensure total hours do not exceed 8 per day
        if self.hours_spent > 8:
            raise ValueError("You cannot log more than 8 hours per day.")
        super().save(*args, **kwargs)
