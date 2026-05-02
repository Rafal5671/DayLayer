import json

import redis
from django.conf import settings


def publish_user_registered(email: str, username: str) -> None:
    """Publish user.registered event to Redis."""
    r = redis.from_url(settings.CELERY_BROKER_URL)
    r.publish(
        "user.registered",
        json.dumps(
            {
                "email": email,
                "username": username,
            }
        ),
    )
