from django.shortcuts import render
from rest_framework import viewsets

from .models import Bookmark
from .serializers import BookmarkSerializer
from .tasks import scrape_bookmark


# Create your views here.
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
        scrape_bookmark.delay(bookmark.id)
