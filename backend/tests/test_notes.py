import pytest
from apps.notes.models import Note
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
def note(user):
    return Note.objects.create(
        user=user,
        title="Test note",
        content="Test content",
        tags="test,django",
    )


@pytest.mark.django_db
def test_create_note(auth_client):
    response = auth_client.post(
        "/api/notes/",
        {
            "title": "New note",
            "content": "Some content",
            "tags": "tag1,tag2",
        },
    )
    assert response.status_code == 201
    assert response.data["title"] == "New note"


@pytest.mark.django_db
def test_list_notes(auth_client, note):
    response = auth_client.get("/api/notes/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_note(auth_client, note):
    response = auth_client.get(f"/api/notes/{note.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Test note"


@pytest.mark.django_db
def test_update_note(auth_client, note):
    response = auth_client.put(
        f"/api/notes/{note.id}/",
        {
            "title": "Updated note",
            "content": "Updated content",
            "tags": "updated",
        },
    )
    assert response.status_code == 200
    assert response.data["title"] == "Updated note"


@pytest.mark.django_db
def test_delete_note(auth_client, note):
    response = auth_client.delete(f"/api/notes/{note.id}/")
    assert response.status_code == 204
    assert not Note.objects.filter(id=note.id).exists()


@pytest.mark.django_db
def test_note_belongs_to_user(client, db):
    other_user = User.objects.create_user(
        username="other",
        email="other@example.com",
        password="TestPass123",
    )
    note = Note.objects.create(user=other_user, title="Other note", content="")

    response = client.post(
        "/api/users/login/",
        {
            "username": "other",
            "password": "TestPass123",
        },
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    main_user = User.objects.create_user(
        username="main",
        email="main@example.com",
        password="TestPass123",
    )
    response = client.post(
        "/api/users/login/",
        {
            "username": "main",
            "password": "TestPass123",
        },
    )
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    response = client.get(f"/api/notes/{note.id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_unauthenticated_cannot_list_notes(client):
    response = client.get("/api/notes/")
    assert response.status_code == 401
