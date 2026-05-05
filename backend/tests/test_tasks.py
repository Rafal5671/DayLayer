import pytest
from apps.tasks.models import Task
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPass123",
    )


@pytest.fixture
def auth_client(client, user):
    response = client.post(
        "/api/users/login/",
        {
            "username": "testuser",
            "password": "TestPass123",
        },
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def task(user):
    return Task.objects.create(
        user=user,
        title="Test task",
        description="Test description",
        priority=Task.Priority.HIGH,
        status=Task.Status.TODO,
    )


@pytest.mark.django_db
def test_create_task(auth_client):
    response = auth_client.post(
        "/api/tasks/",
        {
            "title": "New task",
            "description": "Description",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    assert response.data["title"] == "New task"
    assert response.data["status"] == "todo"


@pytest.mark.django_db
def test_list_tasks(auth_client, task):
    response = auth_client.get("/api/tasks/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_filter_tasks_by_status(auth_client, task):
    response = auth_client.get("/api/tasks/?status=todo")
    assert response.status_code == 200
    assert len(response.data) == 1

    response = auth_client.get("/api/tasks/?status=done")
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_update_task_status(auth_client, task):
    response = auth_client.patch(f"/api/tasks/{task.id}/", {"status": "done"})
    assert response.status_code == 200
    assert response.data["status"] == "done"


@pytest.mark.django_db
def test_complete_task_action(auth_client, task):
    response = auth_client.patch(f"/api/tasks/{task.id}/complete/")
    assert response.status_code == 200
    assert response.data["status"] == "done"


@pytest.mark.django_db
def test_delete_task(auth_client, task):
    response = auth_client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == 204
    assert not Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_unauthenticated_cannot_list_tasks(client):
    response = client.get("/api/tasks/")
    assert response.status_code == 401
