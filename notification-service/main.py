import asyncio
import json
import os
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from dotenv import load_dotenv
from fastapi import FastAPI
from handlers.bookmark import handle_bookmark_scraped
from handlers.task import handle_task_deadline
from handlers.user import handle_user_registered

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

HANDLERS = {
    "user.registered": handle_user_registered,
    "bookmark.scraped": handle_bookmark_scraped,
    "task.deadline_today": handle_task_deadline,
}


async def listen_for_events() -> None:
    """Listen to Redis channels for notification events."""
    redis = await aioredis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    await pubsub.subscribe(*HANDLERS.keys())

    print(f"Notification service listening on: {list(HANDLERS.keys())}")

    try:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message is not None:
                try:
                    channel = message["channel"].decode()
                    data = json.loads(message["data"])
                    print(f"Received event: {channel} | data: {data}")
                    handler = HANDLERS.get(channel)
                    if handler:
                        await handler(data)
                except Exception as e:
                    print(f"Error processing event: {e}")

            await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        await pubsub.unsubscribe(*HANDLERS.keys())
        await redis.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(listen_for_events())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Daylayer Notification Service", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification"}
