# Exam Prep Project - Development Plan

## Instructions for LLM

You are assisting in building a Django-based web application for exam preparation called "exam_prep". This file contains a structured plan for building the project through 15 distinct git commits. Each commit specifies exactly which files to create or modify, with clear paths and detailed descriptions.

Follow these instructions carefully:
1. Create a new directory for the project and work step-by-step through each commit
2. Make sure to create all files with the exact paths specified
3. Use the detailed descriptions to understand what to implement
4. When code snippets are provided, implement them exactly as shown
5. For other implementation details, use your knowledge of Django best practices
6. After each step, commit the changes with the provided commit message

## Development Plan

### Commit 1: Project Initialization and Virtual Environment Setup

**Commit Message:** Initial project setup with virtual environment

**Actions:**
- Create project directory and initialize git
- Set up Python virtual environment
- Create requirements.txt with initial dependencies
- Create .gitignore file

**Files to create/modify:**
- `requirements.txt` - Add Django, django-allauth, psycopg2-binary, Pillow, etc.
- `.gitignore` - Standard Python/Django gitignore patterns

**Notes:**
- Use Python 3.9+ for the virtual environment
- Initial dependencies should include Django 5.0+, django-allauth, psycopg2-binary, Pillow, django-crispy-forms, crispy-bootstrap5

### Commit 2: Django Project Structure Creation

**Commit Message:** Create Django project structure

**Actions:**
- Initialize Django project using django-admin
- Configure settings.py with basic project configuration
- Create main apps: core and users

**Files to create/modify:**
- `manage.py` - Django management script
- `exam_prep/__init__.py` - Empty init file
- `exam_prep/settings.py` - Configure database, installed apps, templates, static files
- `exam_prep/urls.py` - Main URL configuration
- `exam_prep/asgi.py` - ASGI configuration
- `exam_prep/wsgi.py` - WSGI configuration
- `core/__init__.py` - Empty init file
- `core/apps.py` - Core app configuration
- `users/__init__.py` - Empty init file
- `users/apps.py` - Users app configuration

**Notes:**
- Add 'core' and 'users' to INSTALLED_APPS in settings.py
- Configure database to use SQLite for development
- Set up templates and static files directories

### Commit 3: User Authentication Implementation

**Commit Message:** User authentication implementation

**Actions:**
- Set up custom user model
- Create registration and login forms
- Implement authentication views
- Set up authentication templates
- Configure authentication URLs
- Update settings.py for authentication

**Files to create/modify:**
- `users/models.py` - Implement CustomUser model
- `users/forms.py` - Create UserRegisterForm and UserLoginForm
- `users/views.py` - Implement RegisterView and CustomLoginView
- `users/urls.py` - Add authentication URL patterns
- `templates/registration/login.html` - Login form template
- `templates/registration/register.html` - Registration form template
- `exam_prep/settings.py` - Update for authentication (AUTH_USER_MODEL, etc.)

**Notes:**
- User model should extend AbstractUser
- Configure LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL
- Add Argon2 password hasher to settings

### Commit 4: Core Models Implementation

**Commit Message:** Implement core models for exam system

**Actions:**
- Create models for subjects, tests, questions, and answers
- Register models in admin.py
- Create and apply migrations

**Files to create/modify:**
- `core/models.py` - Implement Subject, Test, Question, and Answer models
- `core/admin.py` - Register models in admin site
- Run migrations

**Notes:**
- Question model should support multiple question types (MC, OA, ORD)
- Test model should include fields for randomization settings

### Commit 5: Base Templates and Static Files

**Commit Message:** Add base templates and static files

**Actions:**
- Create base template with navigation
- Set up static files (CSS, JS)
- Configure template inheritance

**Files to create/modify:**
- `templates/base.html` - Main base template with Bootstrap
- `static/css/main.css` - Main CSS file
- `static/js/main.js` - Main JS file
- `templates/includes/navbar.html` - Navigation component

**Notes:**
- Use Bootstrap for basic styling
- Include responsive navigation

### Commit 6: Homepage and Dashboard Views

**Commit Message:** Implement homepage and dashboard views

**Actions:**
- Create homepage view and template
- Implement user dashboard
- Set up URL patterns for homepage and dashboard

**Files to create/modify:**
- `core/views.py` - Add homepage and dashboard views
- `core/urls.py` - Configure URLs for homepage and dashboard
- `templates/core/home.html` - Homepage template
- `templates/core/dashboard.html` - User dashboard template
- `exam_prep/urls.py` - Include core URLs

**Notes:**
- Homepage should be accessible to all users
- Dashboard should require login
- Dashboard should display user's test history and available tests

### Commit 7: Subject and Test List Views

**Commit Message:** Add subject and test listing functionality

**Actions:**
- Implement views for listing subjects and tests
- Create templates for subject and test lists
- Configure URL patterns

**Files to create/modify:**
- `core/views.py` - Add SubjectListView and TestListView
- `core/urls.py` - Add URLs for subject and test lists
- `templates/core/subject_list.html` - Template for subject list
- `templates/core/test_list.html` - Template for test list

**Notes:**
- Subject list should show all available subjects
- Test list should filter tests by subject
- Show only published tests to regular users

### Commit 8: Test Taking Functionality - Part 1

**Commit Message:** Implement basic test taking functionality

**Actions:**
- Create views for starting and taking tests
- Implement question display
- Set up session handling for test progress

**Files to create/modify:**
- `core/views.py` - Add test_start and question_view functions
- `core/urls.py` - Add URLs for test taking
- `templates/core/test_start.html` - Start test template
- `templates/core/question.html` - Question display template

**Notes:**
- Store test progress in session
- Implement basic navigation between questions

### Commit 9: Test Taking Functionality - Part 2

**Commit Message:** Complete test taking and result handling

**Actions:**
- Implement answer submission and validation
- Create test results view and storage
- Add test completion functionality

**Files to create/modify:**
- `core/views.py` - Add submit_answer and test_result views
- `core/models.py` - Add TestResult and TestAnswer models
- `core/urls.py` - Add URLs for answer submission and results
- `templates/core/test_result.html` - Test results template
- Apply migrations for new models

**Notes:**
- Store user answers and calculate score
- Show correct answers on results page
- Track time spent on test

### Commit 10: User Profile Management

**Commit Message:** Add user profile management functionality

**Actions:**
- Implement user profile view and edit
- Create profile templates
- Add profile picture upload

**Files to create/modify:**
- `users/models.py` - Extend user model with profile fields
- `users/views.py` - Add profile view and edit functionality
- `users/forms.py` - Create profile edit form
- `users/urls.py` - Add profile URLs
- `templates/users/profile.html` - User profile template
- `templates/users/profile_edit.html` - Profile edit template

**Notes:**
- Allow users to update profile info and picture
- Use Pillow for image handling
- Apply migrations for profile model changes

### Commit 11: Admin Management Interface

**Commit Message:** Implement admin management interface

**Actions:**
- Create custom admin views for test management
- Implement forms for test creation and editing
- Set up question management interface

**Files to create/modify:**
- `core/views.py` - Add management views for tests and questions
- `core/forms.py` - Create forms for test and question management
- `core/urls.py` - Add management URLs
- `templates/core/management/test_list.html` - Test management list
- `templates/core/management/test_form.html` - Test creation/edit form
- `templates/core/management/question_form.html` - Question management form

**Notes:**
- Restrict access to staff users
- Allow bulk question creation
- Implement drag-and-drop for question ordering

### Commit 12: Advanced Question Types

**Commit Message:** Implement advanced question types and validation

**Actions:**
- Enhance question models and forms
- Implement multiple choice question handling
- Add open answer validation
- Create ordering question functionality

**Files to create/modify:**
- `core/models.py` - Enhance Question and Answer models
- `core/forms.py` - Update question forms for different types
- `core/views.py` - Add type-specific validation logic
- `templates/core/question.html` - Update for different question types
- `static/js/questions.js` - Add JavaScript for question interactions

**Notes:**
- Implement validation for different question types
- Add JavaScript for ordering questions
- Update test taking interface for different question types

### Commit 13: Test Randomization and Settings

**Commit Message:** Add test randomization and configuration options

**Actions:**
- Implement question randomization
- Add answer randomization for MC questions
- Create test configuration options

**Files to create/modify:**
- `core/models.py` - Add randomization fields to Test model
- `core/views.py` - Implement randomization logic in test_start
- `core/forms.py` - Add configuration options to test form
- `templates/core/management/test_form.html` - Update with config options

**Notes:**
- Allow toggling question randomization
- Enable answer randomization for MC questions
- Add time limit configuration

### Commit 14: Styling and UI Improvements

**Commit Message:** Enhance UI with improved styling and interactions

**Actions:**
- Update templates with improved styling
- Add JavaScript for better interactions
- Implement responsive design improvements

**Files to create/modify:**
- `static/css/main.css` - Update main styles
- `static/js/main.js` - Enhance JavaScript functionality
- `templates/base.html` - Update base template
- Update various templates with styling improvements

**Notes:**
- Ensure mobile responsiveness
- Add loading indicators for AJAX operations
- Improve navigation and user flows

### Commit 15: Final Polishing and Documentation

**Commit Message:** Final polishing, testing and documentation

**Actions:**
- Fix any bugs or issues
- Add comprehensive README
- Add documentation comments
- Perform final testing

**Files to create/modify:**
- `README.md` - Comprehensive project documentation
- Add docstrings to Python files
- Update comments in templates and JavaScript
- Fix any remaining issues

**Notes:**
- Include installation instructions in README
- Document system requirements
- Add usage instructions for different user types
- Test all functionality and fix any issues 