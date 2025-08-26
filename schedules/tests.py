from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from django.utils import timezone  # Add this import
from .models import DailySchedule, DailyTask, ProgressStreak, Reminder  # Add Reminder to imports
from tasks.models import Task, Category

User = get_user_model()

class DailyScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='work',
            color='#F9A602'
        )
        self.schedule = DailySchedule.objects.create(
            user=self.user,
            date=date.today()
        )
    
    def test_schedule_creation(self):
        """Test creating a daily schedule"""
        self.assertEqual(self.schedule.user.username, 'testuser')
        self.assertEqual(self.schedule.date, date.today())
    
    def test_completion_percentage(self):
        """Test completion percentage calculation"""
        # Create some tasks
        DailyTask.objects.create(
            schedule=self.schedule,
            title='Task 1',
            category=self.category,
            start_time='09:00:00',
            end_time='10:00:00',
            is_completed=True
        )
        DailyTask.objects.create(
            schedule=self.schedule,
            title='Task 2',
            category=self.category,
            start_time='10:00:00',
            end_time='11:00:00',
            is_completed=False
        )
        
        self.assertEqual(self.schedule.completed_tasks_count, 1)
        self.assertEqual(self.schedule.total_tasks_count, 2)
        self.assertEqual(self.schedule.completion_percentage, 50)


class ProgressStreakModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.streak = ProgressStreak.objects.create(
            user=self.user,
            current_streak=5,
            longest_streak=10
        )
    
    def test_streak_creation(self):
        """Test creating a progress streak"""
        self.assertEqual(self.streak.user.username, 'testuser')
        self.assertEqual(self.streak.current_streak, 5)
        self.assertEqual(self.streak.longest_streak, 10)


class ReminderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='work',
            color='#F9A602'
        )
        self.schedule = DailySchedule.objects.create(
            user=self.user,
            date=date.today()
        )
        self.task = DailyTask.objects.create(
            schedule=self.schedule,
            title='Test Task',
            category=self.category,
            start_time='09:00:00',
            end_time='10:00:00'
        )
        self.reminder = Reminder.objects.create(
            user=self.user,
            task=self.task,
            reminder_time=timezone.now() + timedelta(minutes=30)
        )
    
    def test_reminder_creation(self):
        """Test creating a reminder"""
        self.assertEqual(self.reminder.user.username, 'testuser')
        self.assertEqual(self.reminder.task.title, 'Test Task')
        self.assertFalse(self.reminder.is_sent)


class ScheduleAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_todays_schedule(self):
        """Test getting today's schedule"""
        url = reverse('today-schedule')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('date', response.data)
        self.assertIn('daily_tasks', response.data)
    
    def test_get_progress_stats(self):
        """Test getting progress statistics"""
        url = reverse('progress-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('today', response.data)
        self.assertIn('streak', response.data)
        self.assertIn('weekly_avg', response.data)


class TaskFilterTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='work',
            color='#F9A602'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test tasks
        Task.objects.create(
            user=self.user,
            category=self.category,
            title='Completed Task',
            date=date.today(),
            start_time='09:00:00',
            end_time='10:00:00',
            is_completed=True
        )
        Task.objects.create(
            user=self.user,
            category=self.category,
            title='Pending Task',
            date=date.today(),
            start_time='10:00:00',
            end_time='11:00:00',
            is_completed=False
        )
    
    def test_filter_completed_tasks(self):
        """Test filtering completed tasks"""
        url = reverse('task-list') + '?is_completed=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Completed Task')
    
    def test_filter_by_category(self):
        """Test filtering tasks by category"""
        url = reverse('task-list') + f'?category={self.category.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)