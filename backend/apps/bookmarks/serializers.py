from rest_framework import serializers

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            "id",
            "url",
            "title",
            "description",
            "thumbnail",
            "tags",
            "is_scraped",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "title",
            "description",
            "thumbnail",
            "is_scraped",
            "created_at",
            "updated_at",
        ]
