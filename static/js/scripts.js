// API base URL
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Store authentication token
let authToken = localStorage.getItem('authToken');

// DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function() {
    console.log('Daily Balance app loaded');
    
    // Set up event listeners
    document.getElementById('login-link').addEventListener('click', function(e) {
        e.preventDefault();
        showLoginForm();
    });
    
    document.getElementById('register-link').addEventListener('click', function(e) {
        e.preventDefault();
        showRegisterForm();
    });
    
    document.getElementById('dashboard-link').addEventListener('click', function(e) {
        e.preventDefault();
        if (authToken) {
            showDashboard();
        } else {
            alert('Please login first');
        }
    });
    
    document.getElementById('logout-link').addEventListener('click', function(e) {
        e.preventDefault();
        logout();
    });
    
    // Check if user is already logged in
    if (authToken) {
        document.getElementById('login-link').style.display = 'none';
        document.getElementById('register-link').style.display = 'none';
        document.getElementById('logout-link').style.display = 'inline';
    }
});

// Show/hide functions
function showLoginForm() {
    document.getElementById('home-content').style.display = 'none';
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('auth-forms').style.display = 'block';
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
}

function showRegisterForm() {
    document.getElementById('home-content').style.display = 'none';
    document.getElementById('dashboard').style.display = 'none';
    document.getElementById('auth-forms').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
}

function showDashboard() {
    document.getElementById('home-content').style.display = 'none';
    document.getElementById('auth-forms').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
    loadTasks();
}

function showHome() {
    document.getElementById('home-content').style.display = 'block';
    document.getElementById('auth-forms').style.display = 'none';
    document.getElementById('dashboard').style.display = 'none';
}

function showTaskForm() {
    document.getElementById('task-form').style.display = 'block';
}

// API Functions
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save token and update UI
            authToken = data.access;
            localStorage.setItem('authToken', authToken);
            
            document.getElementById('login-link').style.display = 'none';
            document.getElementById('register-link').style.display = 'none';
            document.getElementById('logout-link').style.display = 'inline';
            
            showDashboard();
        } else {
            alert('Login failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

async function register() {
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const password2 = document.getElementById('reg-password2').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password, password2 })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save token and update UI
            authToken = data.access;
            localStorage.setItem('authToken', authToken);
            
            document.getElementById('login-link').style.display = 'none';
            document.getElementById('register-link').style.display = 'none';
            document.getElementById('logout-link').style.display = 'inline';
            
            showDashboard();
        } else {
            // Show validation errors
            let errorMessage = 'Registration failed: ';
            if (data.username) errorMessage += data.username[0] + ' ';
            if (data.email) errorMessage += data.email[0] + ' ';
            if (data.password) errorMessage += data.password[0] + ' ';
            alert(errorMessage || 'Unknown error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}

async function logout() {
    try {
        const refreshToken = localStorage.getItem('refreshToken');
        await fetch(`${API_BASE_URL}/auth/logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ refresh: refreshToken })
        });
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Clear tokens and update UI
        localStorage.removeItem('authToken');
        localStorage.removeItem('refreshToken');
        authToken = null;
        
        document.getElementById('login-link').style.display = 'inline';
        document.getElementById('register-link').style.display = 'inline';
        document.getElementById('logout-link').style.display = 'none';
        
        showHome();
    }
}

async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/tasks/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const tasks = await response.json();
            displayTasks(tasks);
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

async function createTask() {
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-description').value;
    const start_time = document.getElementById('task-start-time').value;
    const end_time = document.getElementById('task-end-time').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                category: 1, // Default to first category
                title,
                description,
                start_time,
                end_time,
                priority: 'medium',
                is_recurring: false
            })
        });
        
        if (response.ok) {
            // Clear form and reload tasks
            document.getElementById('task-form').style.display = 'none';
            document.getElementById('task-title').value = '';
            document.getElementById('task-description').value = '';
            loadTasks();
        } else {
            const errorData = await response.json();
            alert('Failed to create task: ' + JSON.stringify(errorData));
        }
    } catch (error) {
        console.error('Error creating task:', error);
        alert('Failed to create task. Please try again.');
    }
}

function displayTasks(tasks) {
    const tasksContainer = document.getElementById('tasks-container');
    tasksContainer.innerHTML = '';
    
    if (tasks.length === 0) {
        tasksContainer.innerHTML = '<p>No tasks yet. Add your first task!</p>';
        return;
    }
    
    tasks.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.innerHTML = `
            <h3>${task.title}</h3>
            <p>${task.description || 'No description'}</p>
            <p>Time: ${task.start_time} - ${task.end_time}</p>
            <hr>
        `;
        tasksContainer.appendChild(taskElement);
    });
}