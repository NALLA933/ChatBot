"""
MongoDB connection module using Motor (async driver).
Supports Python 3.10+ with modern type hints.
"""

from typing import Optional
import motor.motor_asyncio
from config import MONGO_URI, DB_NAME

# ──── MongoDB Connection (Module-level globals) ────
_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
db: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None


async def connect_db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    """
    Connect to MongoDB Atlas via Motor (async).
    
    Returns:
        The connected database instance.
        
    Raises:
        Exception: If connection to MongoDB fails.
    """
    global _client, db
    _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = _client[DB_NAME]
    
    # Verify connection
    await _client.admin.command("ping")
    
    # Create TTL index for sticker_packs (auto-expire after 7 days)
    await db.sticker_packs.create_index(
        "saved_at",
        expireAfterSeconds=604800,
    )
    return db


def get_db() -> Optional[motor.motor_asyncio.AsyncIOMotorDatabase]:
    """
    Return the database instance.
    
    Returns:
        The connected database instance, or None if not connected.
    """
    return db
