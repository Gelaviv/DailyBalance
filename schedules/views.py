from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import date, timedelta
from .models import DailySchedule, DailyTask, ProgressStreak
from .serializers import DailyScheduleSerializer, DailyTaskSerializer, ProgressStreakSerializer

class DailyScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailySchedule.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Get or create schedule for today
        schedule, created = DailySchedule.objects.get_or_create(
            user=self.request.user,
            date=date.today(),
            defaults={}
        )
        
        # Generate tasks from recurring tasks
        schedule.generate_from_tasks()
        
        serializer.instance = schedule


class DailyScheduleDetailView(generics.RetrieveAPIView):
    serializer_class = DailyScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailySchedule.objects.filter(user=self.request.user)


class DailyTaskUpdateView(generics.UpdateAPIView):
    serializer_class = DailyTaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailyTask.objects.filter(schedule__user=self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        
        # Update streak if task is being marked as completed
        if instance.is_completed:
            streak, created = ProgressStreak.objects.get_or_create(user=self.request.user)
            streak.update_streak(instance.schedule)


class ProgressStreakView(generics.RetrieveAPIView):
    serializer_class = ProgressStreakSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        streak, created = ProgressStreak.objects.get_or_create(user=self.request.user)
        return streak


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todays_schedule(request):
    """Get or create today's schedule"""
    schedule, created = DailySchedule.objects.get_or_create(
        user=request.user,
        date=date.today(),
        defaults={}
    )
    
    # Generate tasks from recurring tasks
    schedule.generate_from_tasks()
    
    serializer = DailyScheduleSerializer(schedule)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progress_stats(request):
    """Get progress statistics"""
    # Get today's schedule
    schedule, created = DailySchedule.objects.get_or_create(
        user=request.user,
        date=date.today(),
        defaults={}
    )
    
    # Get streak
    streak, created = ProgressStreak.objects.get_or_create(user=request.user)
    
    # Get weekly completion stats
    week_ago = date.today() - timedelta(days=7)
    weekly_schedules = DailySchedule.objects.filter(
        user=request.user,
        date__gte=week_ago
    )
    
    weekly_completion = sum(s.completion_percentage for s in weekly_schedules) / weekly_schedules.count() if weekly_schedules.exists() else 0
    
    return Response({
        'today': {
            'completed': schedule.completed_tasks_count,
            'total': schedule.total_tasks_count,
            'percentage': schedule.completion_percentage
        },
        'streak': {
            'current': streak.current_streak,
            'longest': streak.longest_streak
        },
        'weekly_avg': round(weekly_completion, 1)
    })