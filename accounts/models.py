from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True)
    preferred_daily_start_time = models.TimeField(default='06:00:00')
    time_zone = models.CharField(max_length=50, default='UTC')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"