from emails.sender import send_email


async def handle_task_deadline(data: dict) -> None:
    """Handle task.deadline_today event."""
    email = data.get("email")
    username = data.get("username", "there")
    tasks = data.get("tasks", [])
    if not email or not tasks:
        return

    await send_email(
        to=email,
        subject=f"You have {len(tasks)} task(s) due today",
        template="task_deadline.html",
        context={
            "username": username,
            "tasks": tasks,
            "task_count": len(tasks),
        },
    )
