# Enterprise Task Management API

A role-based task management system built with Flask and PostgreSQL. The API supports authentication, authorization, task workflows, project management, and member assignment using JWT-secured endpoints.

## Features

### Authentication & Authorization

* User Registration
* User Login
* JWT Authentication
* Role-Based Access Control (RBAC)

### User Roles

* **Admin**

  * Create Tasks
  * Assign Project Heads
  * Assign Members
  * Delete Tasks
  * View All Tasks

* **Project Head**

  * View Assigned Projects
  * Assign Members to Tasks
  * Update Task Status
  * Update Task Description and Deadline

* **Member**

  * View Assigned Tasks
  * Update Task Status

### Task Management

* Create Tasks
* View Tasks
* Update Tasks
* Delete Tasks
* Assign Project Heads
* Assign Members
* Task Status Tracking

### Workflow

Task Lifecycle:

Created → Assigned → In Progress → Under Review → Completed → Closed

## Tech Stack

### Backend

* Python
* Flask

### Database

* PostgreSQL
* SQLAlchemy ORM
* Alembic Migrations

### Authentication

* Flask-JWT-Extended

## Database Design

### Users

* user_id
* name
* email
* password
* role
* created_at

### Tasks

* task_id
* title
* description
* status
* created_by
* project_head_id
* deadline
* created_at

### Task Assignments

* assign_id
* task_id
* member_id
* assigned_at

## API Endpoints

### Authentication

| Method | Endpoint  |
| ------ | --------- |
| POST   | /register |
| POST   | /login    |
| GET    | /profile  |

### Users

| Method | Endpoint              |
| ------ | --------------------- |
| GET    | /users                |
| POST   | /users/<user_id>/role |

### Tasks

| Method | Endpoint                       |
| ------ | ------------------------------ |
| GET    | /tasks                         |
| GET    | /tasks/<task_id>               |
| POST   | /tasks                         |
| PUT    | /tasks/<task_id>               |
| DELETE | /tasks/<task_id>               |
| POST   | /tasks/<task_id>/assign-head   |
| POST   | /tasks/<task_id>/assign-member |

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd enterprise-task-management-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Database Migrations

```bash
flask --app run.py db upgrade
```

### Run Application

```bash
python run.py
```

## Future Enhancements

* Activity Logs
* Audit Trail
* Dashboard APIs
* Notifications
* Docker Support
* Automated Testing
* CI/CD Pipeline

## Author

Sanyog Faujdar
