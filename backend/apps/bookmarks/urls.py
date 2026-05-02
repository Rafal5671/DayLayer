from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookmarkViewSet

router = DefaultRouter()
router.register(r"", BookmarkViewSet, basename="bookmarks")

urlpatterns = [
    path("", include(router.urls)),
]
