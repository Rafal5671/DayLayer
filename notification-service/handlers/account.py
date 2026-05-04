from emails.sender import send_email


async def handle_password_changed(data: dict) -> None:
    """Handle account.password_changed event."""
    email = data.get("email")
    username = data.get("username")
    if not email:
        return

    await send_email(
        to=email,
        subject="Your password has been changed",
        template="password_changed.html",
        context={"username": username},
    )


async def handle_profile_updated(data: dict) -> None:
    """Handle account.profile_updated event."""
    email = data.get("email")
    username = data.get("username")
    changes = data.get("changes", [])
    if not email:
        return

    await send_email(
        to=email,
        subject="Your profile has been updated",
        template="profile_updated.html",
        context={"username": username, "changes": changes},
    )


async def handle_account_deleted(data: dict) -> None:
    """Handle account.deleted event."""
    email = data.get("email")
    username = data.get("username")
    if not email:
        return

    await send_email(
        to=email,
        subject="Your account has been deleted",
        template="account_deleted.html",
        context={"username": username},
    )
