from django.db import models
from accounts.models import User

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
    color = models.CharField(max_length=7, default='#000000')  # Hex color code
    
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.TimeField()  # This should be a TimeField
    end_time = models.TimeField()    # This should be a TimeField
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_recurring = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"
    
    def duration(self):
        # Calculate duration in hours
        # Make sure start_time and end_time are time objects, not strings
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