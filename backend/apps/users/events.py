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


def publish_password_changed(email: str, username: str) -> None:
    """Publish account.password_changed event to Redis."""
    r = redis.from_url(settings.CELERY_BROKER_URL)
    r.publish(
        "account.password_changed", json.dumps({"email": email, "username": username})
    )


def publish_profile_updated(email: str, username: str, changes: list) -> None:
    """Publish account.profile_updated event to Redis."""
    r = redis.from_url(settings.CELERY_BROKER_URL)
    r.publish(
        "account.profile_updated",
        json.dumps(
            {
                "email": email,
                "username": username,
                "changes": changes,
            }
        ),
    )


def publish_account_deleted(email: str, username: str) -> None:
    """Publish account.deleted event to Redis."""
    r = redis.from_url(settings.CELERY_BROKER_URL)
    r.publish("account.deleted", json.dumps({"email": email, "username": username}))
