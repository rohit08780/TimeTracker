# tasks/views.py

from rest_framework import viewsets
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer
from rest_framework.decorators import action,api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import csv
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from datetime import date
from rest_framework.exceptions import AuthenticationFailed


from rest_framework.exceptions import AuthenticationFailed

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        
        # Check if the user is authenticated
        if not user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated")

        if user.role == 'employee':
            return Task.objects.filter(employee=user)
        return Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        task = self.get_object()
        if task.status == 'pending':
            task.status = 'approved'
            task.save()
            return Response({'status': 'Task approved'})
        return Response({'status': 'Task cannot be approved'}, status=400)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        task = self.get_object()
        task.status = 'rejected'
        task.manager_comment = request.data.get('comment', '')
        task.save()
        return Response({'status': 'Task rejected'})


@login_required
def manager_dashboard(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')
        comment = request.POST.get('manager_comment')
        task = Task.objects.get(id=task_id)
        task.status = 'approved' if action == 'approve' else 'rejected'
        task.manager_comment = comment
        task.save()
        return redirect('manager_dashboard')

    pending_tasks = Task.objects.filter(status='pending')
    return render(request, 'manager_dashboard.html', {'pending_tasks': pending_tasks})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_progress_report(request):
    if request.user.role != 'manager':
        return Response({'error': 'Access denied'}, status=403)

    tasks = Task.objects.all()
    report = {}

    for task in tasks:
        emp = task.employee.username
        week = task.date.isocalendar()[1]
        key = (emp, week)

        if key not in report:
            report[key] = 0
        report[key] += task.hours_spent

    return Response([
        {'employee': emp, 'week': week, 'hours': hours}
        for (emp, week), hours in report.items()
    ])




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_csv_report(request):
    tasks = Task.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="task_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee', 'Title', 'Date', 'Hours', 'Status'])

    for task in tasks:
        writer.writerow([task.employee.username, task.title, task.date, task.hours_spent, task.status])

    return response



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filtered_report(request):
    queryset = Task.objects.all()

    tag = request.GET.get('tag')
    status = request.GET.get('status')
    min_time = request.GET.get('min_time')

    if tag:
        queryset = queryset.filter(description__icontains=tag)
    if status:
        queryset = queryset.filter(status=status)
    if min_time:
        queryset = queryset.filter(hours_spent__gte=min_time)

    data = TaskSerializer(queryset, many=True).data
    return Response(data)


