from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model. Timestamps are read-only."""

    class Meta:
        model = Note
        fields = ["id", "title", "content", "tags", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
