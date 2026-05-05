from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    """
    Represents a user note with Markdown content and tags.

    Notes are ordered by last update time, newest first.
    Each note belongs to a single user and is not visible to others.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
