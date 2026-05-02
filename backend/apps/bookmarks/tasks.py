import requests
from bs4 import BeautifulSoup
from celery import shared_task

from .models import Bookmark


@shared_task
def scrape_bookmark(bookmark_id):
    try:
        bookmark = Bookmark.objects.get(id=bookmark_id)
        response = requests.get(bookmark.url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        og_title = soup.find("meta", property="og:title")
        bookmark.title = (
            og_title["content"]
            if og_title
            else (soup.title.string if soup.title else bookmark.url)
        )

        # Description
        og_desc = soup.find("meta", property="og:description")
        if og_desc:
            bookmark.description = og_desc["content"]

        # Thumbnail
        og_image = soup.find("meta", property="og:image")
        if og_image:
            bookmark.thumbnail = og_image["content"]

        bookmark.is_scraped = True
        bookmark.save()

    except Exception:
        pass
