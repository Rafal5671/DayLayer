import asyncio
import json
import os
from contextlib import asynccontextmanager

import httpx
import redis.asyncio as aioredis
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DJANGO_API_URL = os.getenv("DJANGO_API_URL", "http://localhost:8000/api")


def scrape_url(url: str) -> dict:
    """Scrape metadata from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        og_title = soup.find("meta", property="og:title")
        og_desc = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")

        return {
            "title": (
                og_title["content"]
                if og_title
                else (soup.title.string if soup.title else url)
            ),
            "description": og_desc["content"] if og_desc else "",
            "thumbnail": og_image["content"] if og_image else "",
        }
    except Exception as e:
        print(f"Scraping error: {e}")
        return {"title": url, "description": "", "thumbnail": ""}


async def update_bookmark(bookmark_id: int, data: dict) -> None:
    """Send scraped data back to Django API."""
    secret = os.getenv("INTERNAL_SERVICE_SECRET")
    async with httpx.AsyncClient() as client:
        try:
            await client.patch(
                f"{DJANGO_API_URL}/bookmarks/{bookmark_id}/update_scraped/",
                json=data,
                headers={"X-Internal-Secret": secret},
                timeout=10,
            )
            print(f"Bookmark {bookmark_id} updated successfully")
        except Exception as e:
            print(f"Failed to update bookmark {bookmark_id}: {e}")


async def listen_for_scraping_jobs() -> None:
    """Listen to Redis channel for scraping jobs."""
    redis = await aioredis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    await pubsub.subscribe("bookmark.scrape")

    print("Scraping service listening for jobs...")

    try:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message is not None:
                try:
                    data = json.loads(message["data"])
                    bookmark_id = data["bookmark_id"]
                    url = data["url"]

                    print(f"Scraping bookmark {bookmark_id}: {url}")
                    scraped = scrape_url(url)
                    await update_bookmark(bookmark_id, scraped)

                    await redis.publish(
                        "bookmark.scraped",
                        json.dumps(
                            {
                                "bookmark_id": bookmark_id,
                                "title": scraped["title"],
                            }
                        ),
                    )

                except Exception as e:
                    print(f"Error processing job: {e}")

            await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        await pubsub.unsubscribe("bookmark.scrape")
        await redis.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(listen_for_scraping_jobs())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Daylayer Scraping Service", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "scraping"}
