# Daily Balance - Personal Productivity App

## Overview

Daily Balance is a simple personal productivity app designed to help busy individuals stay organized and spiritually grounded. The app allows users to create a daily routine that includes key life components such as work, study, prayer, and family time.

## Features Implemented
## Core Functionality

### User Authentication System

* User registration with email & password

* JWT-based login/logout functionality

* Profile management (name, preferred daily start time, time zone)

* Secure session management

### Task Management

* Create, read, update, and delete tasks

* Categorized tasks (Spiritual, Family, Study, Work, Personal, Health, Other)

* Time allocation with start and end times

* Priority levels (High/Medium/Low)

* Color-coded categories

### Daily Schedule View

* Tasks displayed in time-sorted list

* Color-coded by category

* Today's tasks view

### Basic Progress Tracking

* Mark tasks as completed

* Completion status tracking

* Basic progress statistics

## Technology Stack
* Backend: Django 4.2.5 + Django REST Framework

* Authentication: JWT (JSON Web Tokens)

* Database: SQLite (development)

* Frontend: Basic HTML/CSS/JS templates

## Project Structure
```
daily-balance/
├── accounts/                 # User authentication app
│   ├── models.py            # Custom User and Profile models
│   ├── serializers.py       # Authentication serializers
│   ├── views.py             # Auth views (register, login, logout)
│   ├── urls.py              # Authentication endpoints
│   └── tests.py             # Comprehensive auth tests
├── tasks/                   # Task management app
│   ├── models.py            # Category and Task models
│   ├── serializers.py       # Task serializers
│   ├── views.py             # Task CRUD operations
│   ├── urls.py              # Task API endpoints
│   └── tests.py             # Task model and API tests
├── schedules/               # Scheduling app (foundation)
│   ├── models.py            # Daily schedule models
│   ├── tests.py             # Schedule tests
│   └── ...                  # Additional schedule functionality
├── static/                  # Static files
│   ├── css/
│   │   └── styles.css       # Application styling
│   └── js/
│       └── scripts.js       # Frontend functionality
├── templates/               # HTML templates
│   └── base.html            # Main template
├── daily_balance/           # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI configuration
└── manage.py                # Django management script
```

# API Endpoints
## Authentication

* POST /api/auth/register/ - User registration

### Headers:

* Content-Type: application/json

```
{
  "username": "testuser3",
  "email": "test3@example.com",
  "password": "testpassword12",
  "password2": "testpassword12",
  "first_name": "Test3",
  "last_name": "User3"
}


**Expected Response: 201 Created**

{
  "user": {
    "id": 1,
    "username": "testuser3",
    "email": "test3@example.com",
    "first_name": "Test3",
    "last_name": "User3"
  },
  "refresh": "eyJ...",
  "access": "eyJ...",
  "message": "User created successfully"
}

```

* POST /api/auth/login/ - User login
### Headers:

* Content-Type: application/json

```
{
  "username": "testuser3",
  "password": "testpassword12"
}


Expected Response: 200 OK

{
  "user": {
    "id": 1,
    "username": "testuser3",
    "email": "test3@example.com",
    "first_name": "Test3",
    "last_name": "User3"
  },
  "refresh": "eyJ...",
  "access": "eyJ...",
  "message": "Login successful"
}

```

* POST /api/auth/logout/ - User logout
### Headers:

* Authorization: Bearer {{access_token}}

* Content-Type: application/json

```
{
  "refresh": "{{refresh_token}}"
}

Expected Response: 200 OK

{
  "message": "Logout successful"
}

```

* GET /api/auth/profile/ - User profile

### Headers:

* Authorization: Bearer {{access_token}}

```
Expected Response: 200 OK

{
  "username": "testuser3",
  "password": "testpassword12"
}
```

* POST /api/auth/change-password/ - Password change

### Headers:

* Authorization: Bearer {{access_token}}

* Content-Type: application/json

```
{
  "old_password": "testpassword12",
  "new_password": "newpassword123"
}
```

## Tasks

* GET /api/tasks/categories/ - List all categories
### Headers:

* Authorization: Bearer {{access_token}}

```
Expected Response: 200 OK

[
  {
    "id": 1,
    "name": "spiritual",
    "color": "#FF6B6B"
  },
  {
    "id": 2,
    "name": "family",
    "color": "#4ECDC4"
  }
]
```

* GET /api/tasks/tasks/ - List user's tasks
### Headers:

* Authorization: Bearer {{access_token}}

```
Expected Response: 200 OK

[
  {
    "id": 1,
    "category": 1,
    "title": "Morning Prayer",
    "description": "Daily morning prayer time",
    "start_time": "06:00:00",
    "end_time": "06:30:00",
    "priority": "high",
    "is_recurring": true,
    "is_completed": false,
    "created_at": "2023-10-05T10:00:00Z",
    "updated_at": "2023-10-05T10:00:00Z",
    "category_name": "spiritual",
    "duration": 0.5
  }
]
```

* POST /api/tasks/tasks/ - Create new task
### Headers:

* Authorization: Bearer {{access_token}}

* Content-Type: application/json
```
{
  "category": 1,
  "title": "Morning Prayer",
  "description": "Daily morning prayer time",
  "start_time": "06:00:00",
  "end_time": "06:30:00",
  "priority": "high",
  "is_recurring": true
}


Expected Response: 201 Created

{
  "id": 1,
  "category": 1,
  "title": "Morning Prayer",
  "description": "Daily morning prayer time",
  "start_time": "06:00:00",
  "end_time": "06:30:00",
  "priority": "high",
  "is_recurring": true,
  "is_completed": false,
  "created_at": "2023-10-05T10:00:00Z",
  "updated_at": "2023-10-05T10:00:00Z",
  "category_name": "spiritual",
  "duration": 0.5
}

```

* GET /api/tasks/tasks/{id}/ - Get specific task

### Headers:

* Authorization: Bearer {{access_token}}

```
Expected Response: 200 OK

{
  "id": 1,
  "category": 1,
  "title": "Morning Prayer",
  "description": "Daily morning prayer time",
  "start_time": "06:00:00",
  "end_time": "06:30:00",
  "priority": "high",
  "is_recurring": true,
  "is_completed": false,
  "created_at": "2023-10-05T10:00:00Z",
  "updated_at": "2023-10-05T10:00:00Z",
  "category_name": "spiritual",
  "duration": 0.5
}
```

* PUT /api/tasks/tasks/{id}/ - Update task

### Headers:

* Authorization: Bearer {{access_token}}

* Content-Type: application/json
```
json
{
  "category": 1,
  "title": "Morning Prayer and Meditation",
  "description": "Daily morning prayer and meditation time",
  "start_time": "06:00:00",
  "end_time": "06:45:00",
  "priority": "high",
  "is_recurring": true
}

Expected Response: 200 OK

{
  "id": 1,
  "category": 1,
  "title": "Morning Prayer and Meditation",
  "description": "Daily morning prayer and meditation time",
  "start_time": "06:00:00",
  "end_time": "06:45:00",
  "priority": "high",
  "is_recurring": true,
  "is_completed": false,
  "created_at": "2023-10-05T10:00:00Z",
  "updated_at": "2023-10-05T10:05:00Z",
  "category_name": "spiritual",
  "duration": 0.75
}
```

* DELETE /api/tasks/tasks/{id}/ - Delete task

### Headers:

* Authorization: Bearer {{access_token}}
```
Expected Response: 204 No Content
```

* GET /api/tasks/tasks/today/ - Get today's tasks
### Headers:

* Authorization: Bearer {{access_token}}

```
Expected Response: 200 OK

[
  {
    "id": 1,
    "category": 1,
    "title": "Morning Prayer",
    "description": "Daily morning prayer time",
    "start_time": "06:00:00",
    "end_time": "06:30:00",
    "priority": "high",
    "is_recurring": true,
    "is_completed": false,
    "created_at": "2023-10-05T10:00:00Z",
    "updated_at": "2023-10-05T10:00:00Z",
    "category_name": "spiritual",
    "duration": 0.5
  }
]

```
## Schedules
* GET /api/schedules/today/ - Get today's schedule

### Headers:

* Authorization: Bearer {{access_token}}

```
Expected Response: 200 OK

{
  "id": 1,
  "user": 1,
  "date": "2023-10-05",
  "created_at": "2023-10-05T00:00:00Z",
  "updated_at": "2023-10-05T00:00:00Z",
  "daily_tasks": [
    {
      "id": 1,
      "title": "Morning Prayer",
      "category": 1,
      "start_time": "06:00:00",
      "end_time": "06:30:00",
      "priority": "high",
      "is_completed": false,
      "category_name": "spiritual",
      "category_color": "#FF6B6B"
    }
  ],
  "completed_tasks_count": 0,
  "total_tasks_count": 1,
  "completion_percentage": 0
}
```

* GET /api/schedules/progress/stats/ - Get progress statistics

### Headers:

* Authorization: Bearer {{access_token}}

```
Expected Response: 200 OK

json
{
  "today": {
    "completed": 0,
    "total": 1,
    "percentage": 0
  },
  "streak": {
    "current": 0,
    "longest": 0
  },
  "weekly_avg": 0
}
```
# Installation & Setup

## Prerequisites

* Python 3.8+
* pip package manager

## Steps
1. Clone the repository

2. Create virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install django djangorestframework djangorestframework-simplejwt pillow

4. Run migrations:
python manage.py migrate

5. Load default categories:
python manage.py load_default_categories

6. Create superuser (optional):
python manage.py createsuperuser

7. Run development server:
python manage.py runserver


## Testing
Run the complete test suite:
python manage.py test

Run tests for specific apps:
python manage.py test accounts
python manage.py test tasks
python manage.py test schedules



# Usage

1. Register a new account at /api/auth/register/

2. Login to get your access token

3. Create tasks with categories, times, and priorities

4. View your daily schedule with color-coded tasks

5. Mark tasks as completed to track progress


# Default Categories

The app includes these predefined categories:

* Spiritual (#FF6B6B - Red)

* Family (#4ECDC4 - Teal)

* Study (#45B7D1 - Blue)

* Work (#F9A602 - Orange)

* Personal (#9B59B6 - Purple)

* Health (#2ECC71 - Green)

* Other (#95A5A6 - Gray)



# Development Status

## Completed Phase 1: Foundation & Authentication

* Project setup with Django and DRF

* JWT authentication system

* User model with profile extension

* Complete testing suite


## Completed Phase 2: Task Management

* Category and Task models

* Full CRUD operations for tasks

* API endpoints for task management

* Comprehensive testing

* Production deployment



## Future Enhancements (Planned)

* Recurring tasks system (started but not completed)

* Advanced reminder functionality (started but not completed)

* Progress streak tracking (started but not completed) 

* Enhanced reporting dashboard (not started)


# Contributing
This is a personal project focused on learning Django and DRF development. The code follows best practices for API development and includes comprehensive testing.

# License
This project is created for educational purposes as part of backend development learning.