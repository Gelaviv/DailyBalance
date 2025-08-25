from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Category, Task

User = get_user_model()

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='spiritual',
            color='#FF6B6B'
        )
    
    def test_category_creation(self):
        """Test creating a category"""
        self.assertEqual(self.category.name, 'spiritual')
        self.assertEqual(self.category.color, '#FF6B6B')
        self.assertEqual(self.category.get_name_display(), 'Spiritual')
    
    def test_category_str_representation(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), 'Spiritual')

class TaskModelTest(TestCase):
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
        self.task = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Test Task',
            description='Test Description',
            start_time='09:00:00',
            end_time='10:00:00',
            priority='high',
            is_recurring=False
        )
    
    def test_task_creation(self):
        """Test creating a task"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        
        # Handle both string and time objects
        if isinstance(self.task.start_time, str):
            self.assertEqual(self.task.start_time, '09:00:00')
        else:
            self.assertEqual(self.task.start_time.strftime('%H:%M:%S'), '09:00:00')
            
        if isinstance(self.task.end_time, str):
            self.assertEqual(self.task.end_time, '10:00:00')
        else:
            self.assertEqual(self.task.end_time.strftime('%H:%M:%S'), '10:00:00')
            
        self.assertEqual(self.task.priority, 'high')
        self.assertFalse(self.task.is_recurring)
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.user.username, 'testuser')
        self.assertEqual(self.task.category.name, 'work')
    
    def test_task_str_representation(self):
        """Test task string representation"""
        self.assertEqual(str(self.task), 'Test Task (testuser)')
    
    def test_task_duration_calculation(self):
        """Test task duration calculation"""
        duration = self.task.duration()
        self.assertEqual(duration, 1.0)  # 1 hour

class CategoryAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='spiritual',
            color='#FF6B6B'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_categories(self):
        """Test retrieving categories"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'spiritual')

class TaskAPITest(APITestCase):
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
    
    def test_create_task(self):
        """Test creating a task via API"""
        url = reverse('task-list')
        data = {
            'category': self.category.id,
            'title': 'API Test Task',
            'description': 'API Test Description',
            'start_time': '09:00:00',
            'end_time': '10:00:00',
            'priority': 'high',
            'is_recurring': False
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'API Test Task')
    
    def test_get_tasks(self):
        """Test retrieving tasks via API"""
        # First create a task
        Task.objects.create(
            user=self.user,
            category=self.category,
            title='Test Task',
            description='Test Description',
            start_time='09:00:00',
            end_time='10:00:00',
            priority='high',
            is_recurring=False
        )
        
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')
    
    def test_get_task_detail(self):
        """Test retrieving a specific task via API"""
        task = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Test Task',
            description='Test Description',
            start_time='09:00:00',
            end_time='10:00:00',
            priority='high',
            is_recurring=False
        )
        
        url = reverse('task-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')
    
    def test_update_task(self):
        """Test updating a task via API"""
        task = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Test Task',
            description='Test Description',
            start_time='09:00:00',
            end_time='10:00:00',
            priority='high',
            is_recurring=False
        )
        
        url = reverse('task-detail', kwargs={'pk': task.id})
        data = {
            'category': self.category.id,
            'title': 'Updated Task',
            'description': 'Updated Description',
            'start_time': '09:00:00',
            'end_time': '10:00:00',
            'priority': 'medium',
            'is_recurring': True
        }
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
        self.assertEqual(task.priority, 'medium')
        self.assertTrue(task.is_recurring)
    
    def test_delete_task(self):
        """Test deleting a task via API"""
        task = Task.objects.create(
            user=self.user,
            category=self.category,
            title='Test Task',
            description='Test Description',
            start_time='09:00:00',
            end_time='10:00:00',
            priority='high',
            is_recurring=False
        )
        
        url = reverse('task-detail', kwargs={'pk': task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)