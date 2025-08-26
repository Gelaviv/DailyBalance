from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User
from datetime import date

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('spiritual', 'Spiritual'),
        ('family', 'Family'),
        ('study', 'Study'),
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    color = models.CharField(max_length=7, default='#000000')
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.get_name_display()


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    RECURRENCE_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(default=date.today)  # Add date field
    start_time = models.TimeField()
    end_time = models.TimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='none')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"
    
    def clean(self):
        # Validate that end time is after start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def duration(self):
        # Calculate duration in hours
        if isinstance(self.start_time, str):
            from datetime import datetime
            start_time = datetime.strptime(self.start_time, '%H:%M:%S').time()
        else:
            start_time = self.start_time
            
        if isinstance(self.end_time, str):
            from datetime import datetime
            end_time = datetime.strptime(self.end_time, '%H:%M:%S').time()
        else:
            end_time = self.end_time
            
        start = start_time.hour + start_time.minute / 60
        end = end_time.hour + end_time.minute / 60
        return round(end - start, 2)
    
    def duplicate_for_date(self, new_date):
        """Create a duplicate task for a specific date"""
        return Task(
            user=self.user,
            category=self.category,
            title=self.title,
            description=self.description,
            date=new_date,
            start_time=self.start_time,
            end_time=self.end_time,
            priority=self.priority,
            is_recurring=self.is_recurring,
            recurrence_pattern=self.recurrence_pattern
        )