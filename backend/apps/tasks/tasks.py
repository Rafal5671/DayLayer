import json

import redis
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Task


@shared_task
def check_deadlines() -> None:
    """Check for tasks due today and publish events to Redis."""
    today = timezone.now().date()
    r = redis.from_url(settings.CELERY_BROKER_URL)

    users_with_deadlines = (
        Task.objects.filter(
            deadline=today,
            status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        )
        .values_list("user", flat=True)
        .distinct()
    )

    for user_id in users_with_deadlines:
        user = User.objects.get(id=user_id)
        tasks = Task.objects.filter(
            user=user,
            deadline=today,
            status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        ).values("title", "priority")

        r.publish(
            "task.deadline_today",
            json.dumps(
                {
                    "email": user.email,
                    "username": user.username,
                    "tasks": list(tasks),
                }
            ),
        )

        print(
            f"Published deadline event for {user.username} with {len(list(tasks))} tasks"
        )
