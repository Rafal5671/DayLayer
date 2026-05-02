from emails.sender import send_email


async def handle_bookmark_scraped(data: dict) -> None:
    """Handle bookmark.scraped event."""
    email = data.get("email")
    title = data.get("title", "your bookmark")
    description = data.get("description", "")
    if not email:
        return

    await send_email(
        to=email,
        subject="Your bookmark is ready!",
        template="bookmark_scraped.html",
        context={"title": title, "description": description},
    )
