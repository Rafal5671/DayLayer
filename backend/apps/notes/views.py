from django.shortcuts import render
from rest_framework import viewsets

from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user notes.

    Provides CRUD operations for notes.
    Each user can only access their own notes.
    """

    serializer_class = NoteSerializer

    def get_queryset(self):
        """Return notes belonging to the authenticated user."""
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the authenticated user as the note owner on creation."""
        serializer.save(user=self.request.user)
