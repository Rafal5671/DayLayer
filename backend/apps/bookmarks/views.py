from django.conf import settings
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bookmark
from .serializers import BookmarkSerializer
from .tasks import publish_scrape_job


class BookmarkViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user bookmarks.

    Provides CRUD operations for bookmarks with optional filtering by tags.
    When a bookmark is created, a scraping job is published to Redis
    so the scraping microservice can fetch metadata automatically.
    """

    serializer_class = BookmarkSerializer

    def get_queryset(self):
        """
        Return bookmarks belonging to the authenticated user.

        Supports optional filtering via query parameters:
        - tags: filter by tag name (case-insensitive partial match)
        """
        queryset = Bookmark.objects.filter(user=self.request.user)
        tags = self.request.query_params.get("tags")
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        return queryset

    def perform_create(self, serializer):
        """
        Save the bookmark and publish a scraping job to Redis.

        The scraping microservice will fetch metadata (title, description,
        thumbnail) and update the bookmark via the update_scraped endpoint.
        """
        bookmark = serializer.save(user=self.request.user)
        publish_scrape_job(bookmark.id, bookmark.url, self.request.user.email)

    @action(detail=True, methods=["patch"], permission_classes=[permissions.AllowAny])
    def update_scraped(self, request, pk=None):
        """
        Internal endpoint for the scraping microservice to update bookmark metadata.

        Protected by a shared secret passed in the X-Internal-Secret header.
        Not intended for direct use by API clients.
        """

        secret = request.headers.get("X-Internal-Secret")
        if secret != settings.INTERNAL_SERVICE_SECRET:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        try:
            bookmark = Bookmark.objects.get(pk=pk)
        except Bookmark.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        bookmark.title = request.data.get("title", bookmark.title)
        bookmark.description = request.data.get("description", bookmark.description)
        bookmark.thumbnail = request.data.get("thumbnail", bookmark.thumbnail)
        bookmark.is_scraped = True
        bookmark.save()
        return Response(BookmarkSerializer(bookmark).data)
