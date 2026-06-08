from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from models.task import TaskLog
from models.flashcard import Flashcard, FlashcardReview
from models.progress import ProgressEntry
from models.content import ContentItem
import os

client: AsyncIOMotorClient = None

async def connect_db():
    global client
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.getenv("MONGODB_DB", "nihongo_app")]
    await init_beanie(
        database=db,
        document_models=[User, TaskLog, Flashcard, FlashcardReview, ProgressEntry, ContentItem]
    )
    print("✅ Connected to MongoDB")

async def close_db():
    global client
    if client:
        client.close()
