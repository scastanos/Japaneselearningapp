import asyncio
import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.content import ContentItem
from models.flashcard import Flashcard, FlashcardReview
from models.progress import ProgressEntry
from models.task import TaskLog
from models.user import User

client: AsyncIOMotorClient | None = None
_initialized = False
_init_lock = asyncio.Lock()


async def connect_db() -> None:
    global client

    mongo_url = os.getenv("MONGODB_URL")
    if not mongo_url:
        raise RuntimeError("MONGODB_URL is not set")

    client = AsyncIOMotorClient(
        mongo_url,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    db = client[os.getenv("MONGODB_DB", "nihongo_app")]
    await init_beanie(
        database=db,
        document_models=[User, TaskLog, Flashcard, FlashcardReview, ProgressEntry, ContentItem],
    )


async def ensure_db() -> None:
    """Lazy init for Vercel serverless — lifespan is unreliable on cold starts."""
    global _initialized

    if _initialized:
        return

    async with _init_lock:
        if _initialized:
            return
        await connect_db()
        _initialized = True


async def ping_db() -> bool:
    await ensure_db()
    if not client:
        return False
    await client.admin.command("ping")
    return True


async def close_db() -> None:
    global client, _initialized
    if client:
        client.close()
        client = None
    _initialized = False
