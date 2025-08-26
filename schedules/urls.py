from django.urls import path
from . import views





urlpatterns = [
    path('schedules/', views.DailyScheduleListCreateView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', views.DailyScheduleDetailView.as_view(), name='schedule-detail'),
    path('schedules/today/', views.todays_schedule, name='today-schedule'),
    path('tasks/<int:pk>/', views.DailyTaskUpdateView.as_view(), name='daily-task-update'),
    path('progress/streak/', views.ProgressStreakView.as_view(), name='progress-streak'),
    path('progress/stats/', views.progress_stats, name='progress-stats'),
]