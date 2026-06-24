"""
User and group management for the bot.
Stores user and group information in MongoDB.
"""

from datetime import datetime, timezone
from typing import Any, Optional
from database.connection import get_db


# ═══════════════════════════════════════════════════════
#  USERS COLLECTION
# ═══════════════════════════════════════════════════════

async def upsert_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None
) -> None:
    """
    Insert or update a user in the users collection.
    
    Args:
        user_id: User's Telegram ID.
        username: User's Telegram username (without @).
        first_name: User's first name.
    """
    db = get_db()
    await db.users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "chat_type": "private",
                "is_banned": False,
            },
            "$setOnInsert": {
                "joined_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )


async def get_user(user_id: int) -> Optional[dict[str, Any]]:
    """
    Get a single user document.
    
    Args:
        user_id: User's Telegram ID.
        
    Returns:
        User document dictionary or None if not found.
    """
    db = get_db()
    return await db.users.find_one({"user_id": user_id})


async def get_all_users() -> list[dict[str, Any]]:
    """
    Return all users from users collection.
    
    Returns:
        List of all user documents.
    """
    db = get_db()
    return await db.users.find().to_list(length=None)


async def get_total_users() -> int:
    """
    Count total users.
    
    Returns:
        Total number of registered users.
    """
    db = get_db()
    return await db.users.count_documents({})


# ═══════════════════════════════════════════════════════
#  GROUPS COLLECTION (separate from users!)
# ═══════════════════════════════════════════════════════

async def upsert_group(
    chat_id: int,
    chat_title: Optional[str] = None,
    username: Optional[str] = None
) -> None:
    """
    Insert or update a group in the groups collection.
    
    Args:
        chat_id: Group's Telegram chat ID.
        chat_title: Group's title/name.
        username: Group's username (if public, without @).
    """
    db = get_db()
    await db.groups.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "chat_id": chat_id,
                "chat_title": chat_title,
                "username": username,
                "is_banned": False,
            },
            "$setOnInsert": {
                "added_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )


async def get_all_groups() -> list[dict[str, Any]]:
    """
    Return all groups from groups collection.
    
    Returns:
        List of all group documents.
    """
    db = get_db()
    return await db.groups.find().to_list(length=None)


async def get_total_groups() -> int:
    """
    Count total groups.
    
    Returns:
        Total number of registered groups.
    """
    db = get_db()
    return await db.groups.count_documents({})


# ═══════════════════════════════════════════════════════
#  AI_USERS COLLECTION (separate — only for AI tracking)
# ═══════════════════════════════════════════════════════

async def upsert_ai_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None
) -> None:
    """
    Insert or update a user in the ai_users collection (AI chat tracking only).
    
    Args:
        user_id: User's Telegram ID.
        username: User's Telegram username.
        first_name: User's first name.
    """
    db = get_db()
    await db.ai_users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_chat": datetime.now(timezone.utc),
            },
            "$setOnInsert": {
                "user_id": user_id,
                "total_chats": 0,
                "ai_joined_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )
                "first_chat": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )


async def get_ai_user(user_id: int) -> dict | None:
    """Get a single AI user document."""
    db = get_db()
    return await db.ai_users.find_one({"user_id": user_id})
