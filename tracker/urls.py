# tracker/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskViewSet
from . import views
from .views import filtered_report,export_csv_report,weekly_progress_report

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('manager/dashboard/', views.manager_dashboard, name='manager-dashboard'),
    path('reports/filter/', filtered_report, name='filtered-report'),
    path('reports/export-csv/', export_csv_report, name='export-csv-report'),
    path('reports/weekly-progress/', weekly_progress_report, name='weekly-progress-report'),

]

