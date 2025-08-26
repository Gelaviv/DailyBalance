from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from tasks.models import Task
from datetime import date, timedelta

class DailySchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_schedules')
    date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username}'s Schedule for {self.date}"
    
    @property
    def completed_tasks_count(self):
        return self.daily_tasks.filter(is_completed=True).count()
    
    @property
    def total_tasks_count(self):
        return self.daily_tasks.count()
    
    @property
    def completion_percentage(self):
        if self.total_tasks_count == 0:
            return 0
        return round((self.completed_tasks_count / self.total_tasks_count) * 100)
    
    def generate_from_tasks(self):
        """Generate daily tasks from user's recurring tasks"""
        # Get all recurring tasks for this user
        recurring_tasks = Task.objects.filter(
            user=self.user, 
            is_recurring=True,
            date__lte=self.date  # Tasks that should have started by this date
        )
        
        for task in recurring_tasks:
            # Check if this task should occur on this date based on recurrence pattern
            if self.should_occur_today(task):
                # Create or get the daily task
                daily_task, created = DailyTask.objects.get_or_create(
                    schedule=self,
                    original_task=task,
                    defaults={
                        'title': task.title,
                        'category': task.category,
                        'start_time': task.start_time,
                        'end_time': task.end_time,
                        'priority': task.priority,
                    }
                )

    def should_occur_today(self, task):
        """Check if a recurring task should occur on this date"""
        if not task.is_recurring:
            return False
        
        days_diff = (self.date - task.date).days
        
        if task.recurrence_pattern == 'daily':
            return days_diff >= 0  # Every day from start date
        
        elif task.recurrence_pattern == 'weekly':
            return days_diff >= 0 and days_diff % 7 == 0  # Same day each week
        
        elif task.recurrence_pattern == 'monthly':
            # Simple monthly recurrence (same day of month)
            return days_diff >= 0 and self.date.day == task.date.day
        
        return False


class DailyTask(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    schedule = models.ForeignKey(DailySchedule, on_delete=models.CASCADE, related_name='daily_tasks')
    original_task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey('tasks.Category', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_completed = models.BooleanField(default=False)  # FIXED: Changed from is_completedfield to is_completed
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.title} ({self.schedule.date})"
    
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")
    
    def save(self, *args, **kwargs):
        self.clean()
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)
    
    def duration(self):
        # Calculate duration in hours
        start = self.start_time.hour + self.start_time.minute / 60
        end = self.end_time.hour + self.end_time.minute / 60
        return round(end - start, 2)


class ProgressStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress_streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Streak: {self.current_streak} days"
    
    def update_streak(self, schedule):
        """Update streak based on daily schedule completion"""
        if schedule.completion_percentage >= 80:  # Consider day successful if 80%+ completed
            if self.last_updated == date.today() - timedelta(days=1):
                # Consecutive day
                self.current_streak += 1
            elif self.last_updated < date.today() - timedelta(days=1):
                # Broken streak
                self.current_streak = 1
            # else: already updated today
            
            # Update longest streak if needed
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
            
            self.last_updated = date.today()
            self.save()
        else:
            # Broken streak
            self.current_streak = 0
            self.last_updated = date.today()
            self.save()



class Reminder(models.Model):
    REMINDER_TYPE_CHOICES = [
        ('notification', 'Notification'),
        ('email', 'Email'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    task = models.ForeignKey(DailyTask, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES, default='notification')
    reminder_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['reminder_time']
    
    def __str__(self):
        return f"Reminder for {self.task.title} at {self.reminder_time}"
    
    def should_send_now(self):
        return not self.is_sent and timezone.now() >= self.reminder_time