from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bookmark
from .serializers import BookmarkSerializer
from .tasks import publish_scrape_job


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        queryset = Bookmark.objects.filter(user=self.request.user)
        tags = self.request.query_params.get("tags")
        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        return queryset

    def perform_create(self, serializer):
        bookmark = serializer.save(user=self.request.user)
        publish_scrape_job(bookmark.id, bookmark.url)
        @action(
                detail=True,
                methods=["patch"],
                permission_classes=[permissions.AllowAny]
            )
    def update_scraped(self, request, pk=None):
        """Internal endpoint for scraping service to update bookmark."""
        bookmark = self.get_object()
        bookmark.title = request.data.get("title", bookmark.title)
        bookmark.description = request.data.get("description", bookmark.description)
        bookmark.thumbnail = request.data.get("thumbnail", bookmark.thumbnail)
        bookmark.is_scraped = True
        bookmark.save()
        return Response(BookmarkSerializer(bookmark).data)
