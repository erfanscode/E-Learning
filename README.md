# E-Learning Platform

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/README.md)

A comprehensive e-learning system built with Django, featuring course management, student registration, real-time chat functionality, and more.

## 🌟 Features

- **Course Management**: Create, update, and organize courses by subjects
- **Content Management**: Support for various content types (text, video, files)
- **Student Registration**: User authentication and course enrollment
- **Real-time Chat**: Communication between students and instructors using WebSockets
- **REST API**: API endpoints for programmatic access to the platform
- **Caching**: Redis-based caching for improved performance
- **Responsive Design**: Mobile-friendly user interface

## 🛠️ Technologies

- **Backend**: Django 5.1, Django Channels, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL, Sqlite
- **Cache/Messaging**: Redis
- **WebSockets**: Daphne/ASGI
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx

## 📋 Prerequisites

- Docker and Docker Compose
- Git

## 🚀 Installation & Setup

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/e-learning.git
   cd e-learning
   ```

2. Create an `.env` file based on the example:
   ```bash
   cp .env.example .env
   ```
   
3. Edit the `.env` file with your settings:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=False
   ALLOWED_HOSTS=.localhost,127.0.0.1
   ```

4. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

5. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Access the application:
   - Web interface: http://localhost
   - Admin interface: http://localhost/admin

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/e-learning.git
   cd e-learning
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements.dev.txt  # For development
   ```

4. Create an `.env` file:
   ```bash
   cp .env.example .env
   ```
   
5. Edit the settings in `.env` with your local configuration

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```bash
   python manage.py runserver
   ```

9. Start the Daphne server (for WebSockets):
   ```bash
   daphne -p 8001 education.asgi:application
   ```

## 📝 Project Structure

- `courses/`: Course management functionality
- `students/`: Student registration and course enrollment
- `chat/`: Real-time chat implementation
- `education/`: Project settings and configuration
- `api_examples/`: Examples of API usage
- `static/`: Static files (CSS, JS, images)
- `media/`: User-uploaded files
- `config/`: Configuration files for Nginx, etc.

## 🔐 Authentication

The platform uses Django's built-in authentication system. Users can register as students and instructors can be created via the admin interface.

## 👥 User Roles

- **Admin**: Full access to the platform
- **Instructor**: Can create and manage courses and content
- **Student**: Can enroll in courses and access content

## 📡 API Documentation

The platform provides a RESTful API using Django REST Framework. Endpoints include:

- `/api/courses/`: List and detail views for courses
- `/api/subjects/`: List and detail views for subjects
- `/api/users/`: User management (authentication required)

## 🔄 WebSockets

Real-time chat functionality is implemented using Django Channels and WebSockets. The chat is available for enrolled students and course instructors.

## 🧪 Testing

The platform includes a comprehensive test suite covering models, views, APIs, and WebSocket functionality.

### Running Tests

#### Using Django's test command

```bash
# Run all tests with test settings (recommended)
python manage.py test --settings=education.settings.test

# Run tests for a specific app
python manage.py test courses --settings=education.settings.test
```

#### Using pytest

```bash
# Install pytest and pytest-django
pip install pytest pytest-django

# Run all tests using pytest.ini configuration
python -m pytest

# Run tests with verbose output
python -m pytest -v
```

#### Using Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source=courses,students,chat manage.py test --settings=education.settings.test

# Generate a report
coverage report

# Generate an HTML report
coverage html
# The report will be available in htmlcov/index.html
```

For more detailed information about testing, see [tests/README.md](tests/README.md).

## 🙏 Acknowledgements

- Django Framework and community
- All open-source packages used in this project 