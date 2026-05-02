import json

import redis
from django.conf import settings


def publish_scrape_job(bookmark_id: int, url: str) -> None:
    """Publish scraping job to Redis for scraping service."""
    r = redis.from_url(settings.CELERY_BROKER_URL)
    r.publish(
        "bookmark.scrape",
        json.dumps(
            {
                "bookmark_id": bookmark_id,
                "url": url,
            }
        ),
    )
