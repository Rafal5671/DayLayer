# Daylayer

> A self-hosted personal productivity app for managing notes, tasks and bookmarks.
Built with Django REST Framework, Vue 3 and two independent Python services
communicating via Redis Pub/Sub.

---

## Build Status

![Platform](https://img.shields.io/badge/platform-Web%20App-blue)
![Frontend](https://img.shields.io/badge/frontend-Vue%203-42b883)
![Backend](https://img.shields.io/badge/backend-Django-092e20)
![Database](https://img.shields.io/badge/database-PostgreSQL-336791)
![Auth](https://img.shields.io/badge/authentication-JWT-green)
![Mail](https://img.shields.io/badge/mail-Mailpit-orange)
![Containerized](https://img.shields.io/badge/docker-enabled-2496ed)
![API Docs](https://img.shields.io/badge/API-Swagger-85EA2D)
![Language](https://img.shields.io/badge/language-Python%20%2F%20TypeScript-yellow)
![Tests](https://img.shields.io/badge/tests-pytest-blue)

---

## Description

Daylayer is a full-stack personal productivity application that combines notes, tasks and bookmarks into a single, clean interface. It is built with a Django REST API backend, a Vue 3 frontend, and two independent microservices — a scraping service and a notification service — communicating through Redis Pub/Sub.

When a bookmark is saved, the scraping microservice automatically fetches its title, description. Email notifications are sent on key account events such as registration, password change, profile update and daily task deadlines.

---

## Features

- User registration and login with JWT authentication
- Notes with Markdown support and tag filtering
- Tasks with priority levels, deadlines and status tracking
- Bookmarks with automatic metadata scraping via a dedicated microservice
- Email notifications via a dedicated notification microservice
- Daily deadline reminders via Celery Beat
- Settings panel with profile editing, password change and account deletion
- Swagger API documentation
- Unit and integration tests with pytest
- Dockerized full-stack environment

---

## Tech Stack

- **Frontend:** Vue 3, TypeScript, Pinia, Vue Router, Tailwind CSS, Axios
- **Backend:** Python, Django, Django REST Framework, SimpleJWT, Celery, Celery Beat
- **Scraping Service:** FastAPI, BeautifulSoup4, Redis Pub/Sub
- **Notification Service:** FastAPI, aiosmtplib, Jinja2, Redis Pub/Sub
- **Database:** PostgreSQL
- **Cache / Broker:** Redis
- **Authentication:** JWT
- **Email:** Mailpit (development)
- **API Docs:** Swagger (drf-spectacular)
- **Testing:** pytest, pytest-django, pytest-mock
- **Containerization:** Docker, Docker Compose

---

## Project Structure

```
daylayer/
├── docker-compose.yml
├── backend/                        # Django REST API
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── tests/
│   │   ├── test_users.py
│   │   ├── test_notes.py
│   │   ├── test_tasks.py
│   │   └── test_bookmarks.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── celery.py
│   └── apps/
│       ├── users/                  # Auth, profile, password
│       ├── notes/                  # Notes CRUD
│       ├── tasks/                  # Tasks CRUD with filtering
│       └── bookmarks/              # Bookmarks with scraping integration
├── scraping-service/               # FastAPI microservice
│   ├── Dockerfile
│   └── main.py
├── notification-service/           # FastAPI microservice
│   ├── Dockerfile
│   ├── main.py
│   ├── handlers/
│   │   ├── user.py
│   │   ├── bookmark.py
│   │   ├── task.py
│   │   └── account.py
│   └── emails/
│       ├── sender.py
│       └── templates/
└── frontend/                       # Vue 3 SPA
    ├── Dockerfile
    ├── nginx.conf
    └── src/
        ├── api/
        ├── stores/
        ├── types/
        ├── router/
        ├── components/
        └── views/
```

---

## Architecture

```
┌─────────────┐     HTTP      ┌─────────────────┐     SQL      ┌──────────────┐
│   Vue 3     │ ────────────► │   Django API     │ ──────────► │  PostgreSQL  │
│  Frontend   │               │   (port 8000)    │             └──────────────┘
└─────────────┘               └─────────────────┘
                                       │
                                  Redis Pub/Sub
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                   ▼
           ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
           │   Celery     │  │ Scraping Service  │  │Notification  │
           │   Worker     │  │   (port 8001)     │  │  Service     │
           └──────────────┘  └──────────────────┘  │ (port 8002)  │
                                                    └──────────────┘
                                                           │
                                                           ▼
                                                      ┌─────────┐
                                                      │ Mailpit │
                                                      │  :8025  │
                                                      └─────────┘
```

---

## Getting Started

### Prerequisites

- Docker + Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Rafal5671/DayLayer.git
cd DayLayer
```

### 2. Create `.env` files

```bash
cp backend/.env.example backend/.env
cp scraping-service/.env.example scraping-service/.env
cp notification-service/.env.example notification-service/.env
```

### 3. Run the full stack

```bash
docker compose up --build
```

### 4. Run migrations

```bash
docker compose exec backend python manage.py migrate
```

### 5. Open in browser

| Service              | URL                              |
|----------------------|----------------------------------|
| App                  | http://localhost                 |
| API                  | http://localhost:8000/api        |
| Swagger              | http://localhost:8000/api/docs   |
| Mailpit              | http://localhost:8025            |

---

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

---

## API Overview

| Method | Endpoint                              | Auth     | Description                        |
|--------|---------------------------------------|----------|------------------------------------|
| POST   | /api/users/register/                  | Public   | Register new user                  |
| POST   | /api/users/login/                     | Public   | Login and get JWT token            |
| GET    | /api/users/me/                        | Required | Get current user profile           |
| PATCH  | /api/users/me/                        | Required | Update profile                     |
| DELETE | /api/users/me/                        | Required | Delete account                     |
| POST   | /api/users/change-password/           | Required | Change password                    |
| GET    | /api/notes/                           | Required | List notes                         |
| POST   | /api/notes/                           | Required | Create note                        |
| PUT    | /api/notes/{id}/                      | Required | Update note                        |
| DELETE | /api/notes/{id}/                      | Required | Delete note                        |
| GET    | /api/tasks/                           | Required | List tasks (filterable by status)  |
| POST   | /api/tasks/                           | Required | Create task                        |
| PATCH  | /api/tasks/{id}/                      | Required | Update task                        |
| DELETE | /api/tasks/{id}/                      | Required | Delete task                        |
| GET    | /api/bookmarks/                       | Required | List bookmarks                     |
| POST   | /api/bookmarks/                       | Required | Create bookmark (auto-scraping)    |
| DELETE | /api/bookmarks/{id}/                  | Required | Delete bookmark                    |

Full interactive documentation available at `/api/docs/`.

---

## Email Notifications

| Event                  | Trigger                              |
|------------------------|--------------------------------------|
| Welcome email          | User registration                    |
| Bookmark ready         | Scraping microservice completes      |
| Tasks due today        | Celery Beat runs daily at 8:00 AM    |
| Password changed       | User changes password                |
| Profile updated        | User updates username or email       |
| Account deleted        | User deletes their account           |

---

## Example Screenshots
<img width="1870" height="992" alt="Screenshot 2026-05-11 at 17-11-47 Vite App" src="https://github.com/user-attachments/assets/360cc12a-9a95-4ed9-9d41-df4caa0f4b35" />
<img width="1870" height="992" alt="Screenshot 2026-05-11 at 17-11-56 Vite App" src="https://github.com/user-attachments/assets/b96c5c72-7a92-4edc-8fe3-6faf27911e15" />
<img width="1870" height="992" alt="Screenshot 2026-05-11 at 17-12-03 Vite App" src="https://github.com/user-attachments/assets/cc864cd4-679a-4656-89ed-4f77067985f5" />
<img width="1870" height="992" alt="Screenshot 2026-05-11 at 17-12-09 Vite App" src="https://github.com/user-attachments/assets/2bc8e19a-9d69-4468-92eb-34c2a0cb78d7" />
<img width="1870" height="992" alt="Screenshot 2026-05-11 at 17-12-14 Vite App" src="https://github.com/user-attachments/assets/26a1b2d2-1a2b-4004-8e93-df59d3f79072" />
<img width="922" height="992" alt="Screenshot 2026-05-11 at 17-12-34 Vite App" src="https://github.com/user-attachments/assets/01b0ab1d-aded-42e1-84be-6c094575a928" />

