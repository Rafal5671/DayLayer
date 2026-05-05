import pytest
from apps.bookmarks.models import Bookmark
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
def bookmark(user):
    return Bookmark.objects.create(
        user=user,
        url="https://github.com",
        title="GitHub",
        description="Where the world builds software",
        is_scraped=True,
    )


@pytest.mark.django_db
def test_create_bookmark(auth_client, mocker):
    mocker.patch("apps.bookmarks.views.publish_scrape_job")
    response = auth_client.post(
        "/api/bookmarks/",
        {
            "url": "https://example.com",
        },
    )
    assert response.status_code == 201
    assert response.data["url"] == "https://example.com"


@pytest.mark.django_db
def test_list_bookmarks(auth_client, bookmark):
    response = auth_client.get("/api/bookmarks/")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_filter_bookmarks_by_tag(auth_client, user):
    Bookmark.objects.create(user=user, url="https://a.com", tags="python,django")
    Bookmark.objects.create(user=user, url="https://b.com", tags="vue,frontend")

    response = auth_client.get("/api/bookmarks/?tags=django")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_delete_bookmark(auth_client, bookmark):
    response = auth_client.delete(f"/api/bookmarks/{bookmark.id}/")
    assert response.status_code == 204
    assert not Bookmark.objects.filter(id=bookmark.id).exists()


@pytest.mark.django_db
def test_unauthenticated_cannot_list_bookmarks(client):
    response = client.get("/api/bookmarks/")
    assert response.status_code == 401
