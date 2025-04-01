# E-Learning Platform Tests

This directory contains test utilities and documentation for testing the E-Learning platform.

## Running Tests

### Using the Test Runner

The simplest way to run all tests is to use the test runner script:

```bash
python tests/test_runner.py
```

This will run all tests for all applications and provide a summary of the results.

### Using Django's Test Command

You can also use Django's built-in test command:

```bash
# Run all tests with test settings (recommended)
python manage.py test --settings=education.settings.test

# Run tests for a specific app
python manage.py test courses --settings=education.settings.test
python manage.py test students --settings=education.settings.test
python manage.py test chat --settings=education.settings.test

# Run a specific test class
python manage.py test courses.tests.CourseModelTests --settings=education.settings.test

# Run a specific test method
python manage.py test courses.tests.CourseModelTests.test_course_creation --settings=education.settings.test
```

### Using pytest

For a more flexible and modern test runner:

```bash
# Install pytest and pytest-django
pip install pytest pytest-django

# Run all tests using pytest.ini configuration
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run tests for a specific app
python -m pytest courses/

# Run tests for a specific file
python -m pytest courses/tests.py

# Run a specific test class
python -m pytest courses/tests.py::CourseModelTests

# Run a specific test method
python -m pytest courses/tests.py::CourseModelTests::test_course_creation
```

## Test Coverage

To generate a test coverage report, install `coverage`:

```bash
pip install coverage
```

Then run the tests with coverage:

```bash
# Run tests with coverage
coverage run --source=courses,students,chat manage.py test --settings=education.settings.test

# Generate a report
coverage report

# Generate an HTML report
coverage html
# The report will be available in htmlcov/index.html
```

You can also run pytest with coverage:

```bash
# Install pytest-cov
pip install pytest-cov

# Run pytest with coverage
python -m pytest --cov=courses,students,chat
```

## Test Structure

The tests are organized by application:

- `courses/tests.py`: Tests for course models, views, and functionality
- `students/tests.py`: Tests for student registration and enrollment
- `chat/tests.py`: Tests for the chat functionality
- `courses/api/tests.py`: Tests for the REST API

Each file contains multiple test classes organized by functionality:
- Model tests - Testing data models and relationships
- View tests - Testing HTTP requests and responses
- Permission tests - Testing access control
- API tests - Testing the REST API endpoints

## WebSocket Testing

The chat application uses WebSockets via Django Channels. Testing WebSockets requires setting up the async test environment. 

The commented code in `chat/tests.py` shows how to test WebSocket consumers with an AsyncWebsocketCommunicator, but requires additional setup to run properly.

## Continuous Integration

When running tests in CI environments, use the following command to ensure all tests are discovered and run:

```bash
python -m pytest
```

Or with coverage:

```bash
python -m pytest --cov=courses,students,chat
``` 