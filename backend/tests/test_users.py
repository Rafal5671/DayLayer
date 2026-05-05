import pytest
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


@pytest.mark.django_db
def test_register_success(client):
    response = client.post(
        "/api/users/register/",
        {
            "username": "newuser",
            "email": "new@example.com",
            "password": "NewPass123",
        },
    )
    assert response.status_code == 201
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_duplicate_username(client, user):
    response = client.post(
        "/api/users/register/",
        {
            "username": "testuser",
            "email": "other@example.com",
            "password": "TestPass123",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_short_password(client):
    response = client.post(
        "/api/users/register/",
        {
            "username": "newuser",
            "email": "new@example.com",
            "password": "123",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_success(client, user):
    response = client.post(
        "/api/users/login/",
        {
            "username": "testuser",
            "password": "TestPass123",
        },
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_wrong_password(client, user):
    response = client.post(
        "/api/users/login/",
        {
            "username": "testuser",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_authenticated(auth_client):
    response = auth_client.get("/api/users/me/")
    assert response.status_code == 200
    assert response.data["username"] == "testuser"
    assert response.data["email"] == "test@example.com"


@pytest.mark.django_db
def test_me_unauthenticated(client):
    response = client.get("/api/users/me/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_profile(auth_client):
    response = auth_client.patch(
        "/api/users/me/",
        {
            "username": "updateduser",
            "email": "updated@example.com",
        },
    )
    assert response.status_code == 200
    assert response.data["username"] == "updateduser"


@pytest.mark.django_db
def test_change_password_success(auth_client, user):
    response = auth_client.post(
        "/api/users/change-password/",
        {
            "current_password": "TestPass123",
            "new_password": "NewPass456",
        },
    )
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("NewPass456")


@pytest.mark.django_db
def test_change_password_wrong_current(auth_client):
    response = auth_client.post(
        "/api/users/change-password/",
        {
            "current_password": "wrongpassword",
            "new_password": "NewPass456",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_account(auth_client, user):
    response = auth_client.delete("/api/users/me/")
    assert response.status_code == 204
    assert not User.objects.filter(username="testuser").exists()
