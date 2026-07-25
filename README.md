# Enterprise Task Management API

A production-ready **RESTful Task Management API** built with **Flask**, **PostgreSQL**, and **JWT Authentication**. The application enables organizations to manage projects, assign tasks, control user permissions through Role-Based Access Control (RBAC), and track task activities securely.

The API is containerized using Docker, documented with Swagger, and deployed on Railway using Gunicorn.

---

## Features

### Authentication & Security

- User Registration
- User Login
- JWT Authentication
- Password Hashing
- Protected Routes
- Role-Based Access Control (RBAC)

---

## User Roles

### Admin

- Register users
- View all users
- Change user roles
- Create tasks
- Update tasks
- Delete tasks (Soft Delete)
- Restore deleted tasks
- Assign Project Heads
- View activity logs
- Access dashboard analytics

### Project Head

- View assigned projects
- Assign members to tasks
- Update task details
- Update task status
- View project dashboard

### Member

- View assigned tasks
- Update assigned task status

---

## Task Workflow

```
Created
   │
   ▼
Assigned
   │
   ▼
In Progress
   │
   ▼
Under Review
   │
   ▼
Completed
   │
   ▼
Closed
```

---

# Key Features

- JWT Authentication
- Role-Based Authorization
- Task Management
- Project Head Assignment
- Member Assignment
- Soft Delete & Restore
- Dashboard APIs
- Activity Logs
- Swagger API Documentation
- Database Migrations
- Automatic Owner Seeding
- Docker Support
- Railway Deployment
- Gunicorn Production Server

---

# Tech Stack

## Backend

- Python 3.10
- Flask

## Database

- PostgreSQL
- SQLAlchemy ORM
- Flask-Migrate (Alembic)

## Authentication

- Flask-JWT-Extended

## API Documentation

- Flasgger (Swagger UI)

## Deployment

- Docker
- Gunicorn
- Railway

---

# Project Structure

```
enterprise-task-management-api
│
├── app
│   ├── docs
│   ├── extensions
│   ├── models
│   ├── routes
│   ├── services
│   ├── utils
│   └── config.py
│
├── migrations
├── seed.py
├── start.sh
├── run.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Database Design

## Users

| Field | Description |
|-------|-------------|
| user_id | Primary Key |
| name | User Name |
| email | Unique Email |
| password | Hashed Password |
| role | Admin / Project Head / Member |
| created_at | Account Creation Time |

---

## Tasks

| Field | Description |
|-------|-------------|
| task_id | Primary Key |
| title | Task Title |
| description | Task Description |
| status | Current Status |
| created_by | Task Creator |
| project_head_id | Assigned Project Head |
| deadline | Due Date |
| created_at | Creation Time |
| deleted_at | Soft Delete Timestamp |

---

## Task Assignments

| Field | Description |
|-------|-------------|
| assign_id | Primary Key |
| task_id | Assigned Task |
| member_id | Assigned Member |
| assigned_at | Assignment Time |

---

# API Endpoints

## Authentication

| Method | Endpoint |
|--------|----------|
| POST | `/register` |
| POST | `/login` |
| GET | `/profile` |

---

## Users

| Method | Endpoint |
|--------|----------|
| GET | `/users` |
| POST | `/users/<user_id>/role` |

---

## Tasks

| Method | Endpoint |
|--------|----------|
| GET | `/tasks` |
| GET | `/tasks/<task_id>` |
| POST | `/tasks` |
| PUT | `/tasks/<task_id>` |
| DELETE | `/tasks/<task_id>` |
| PATCH | `/tasks/<task_id>/restore` |
| POST | `/tasks/<task_id>/assign-head` |
| POST | `/tasks/<task_id>/assign-member` |

---

## Dashboard

| Method | Endpoint |
|--------|----------|
| GET | `/dashboard` |

---

## Activity Logs

| Method | Endpoint |
|--------|----------|
| GET | `/logs` |

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/<your-username>/enterprise-task-management-api.git

cd enterprise-task-management-api
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
DATABASE_URL=

SECRET_KEY=

JWT_SECRET_KEY=

OWNER_NAME=

OWNER_EMAIL=

OWNER_PASSWORD=
```

---

## Run Database Migrations

```bash
flask --app run.py db upgrade
```

---

## Seed Owner Account

```bash
python seed.py
```

---

## Run Application

```bash
python run.py
```

---

# Docker

Build and start the application.

```bash
docker compose up --build
```

---

# Production Startup

When deployed, the application automatically:

- Runs pending database migrations
- Creates the default owner account (if it does not exist)
- Starts the application using Gunicorn

---

# API Documentation

Swagger UI

```
/apidocs/
```

Example

```
https://your-domain.up.railway.app/apidocs/
```

---

# Live Demo

**Application**

```
https://railway.com/project/1db794ba-2d70-404b-8f54-96719d4d534c?environmentId=e016a381-2709-43ee-af3e-82a9e7c1a767
```

**Swagger**

```
https://your-domain.up.railway.app/apidocs/
```

---

# Future Improvements

- Email Notifications
- File Attachments
- Background Jobs
- Redis Caching
- WebSocket Notifications
- GitHub Actions CI/CD
- Unit & Integration Testing

---

# Author

**Sanyog Faujdar**

- GitHub: https://github.com/Sanyog-Faujdar
- LinkedIn: https://www.linkedin.com/in/sanyog-faujdar/