"""MongoDB + Redis connection management."""

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

# Global DB client
_mongo_client: AsyncIOMotorClient | None = None
db = None


async def connect_db():
    global _mongo_client, db
    try:
        _mongo_client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=3000,
        )
        await _mongo_client.server_info()  # Test connection
        db = _mongo_client[settings.DATABASE_NAME]
        logger.info("✅ MongoDB connected")

        # Create indexes
        await db.conversations.create_index([("session_id", 1)])
        await db.conversations.create_index([("created_at", -1)])
        await db.feedback.create_index([("timestamp", -1)])

    except Exception as e:
        logger.warning(f"⚠️  MongoDB not available: {e} — running in memory mode")
        db = None


async def disconnect_db():
    global _mongo_client
    if _mongo_client:
        _mongo_client.close()
        logger.info("🔌 MongoDB disconnected")


def get_db():
    return db
