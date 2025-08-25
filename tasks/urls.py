from django.urls import path
from . import views







urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list'),
    path('tasks/today/', views.TodayTaskListView.as_view(), name='today-task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
]