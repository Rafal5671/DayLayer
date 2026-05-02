from emails.sender import send_email


async def handle_user_registered(data: dict) -> None:
    """Handle user.registered event."""
    email = data.get("email")
    username = data.get("username")
    if not email:
        return

    await send_email(
        to=email,
        subject="Welcome to Daylayer!",
        template="welcome.html",
        context={"username": username, "email": email},
    )
