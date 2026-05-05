from django.contrib.auth.models import User
from django.db import models


class Bookmark(models.Model):
    """
    Represents a saved URL with automatically scraped metadata.

    When a bookmark is created, a scraping job is published to Redis.
    The scraping microservice fetches title, description and thumbnail
    and updates the bookmark via the internal update_scraped endpoint.

    Bookmarks are ordered by creation time, newest first.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    is_scraped = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or self.url
