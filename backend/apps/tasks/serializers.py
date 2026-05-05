from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model. Timestamps are read-only."""

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "deadline",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
