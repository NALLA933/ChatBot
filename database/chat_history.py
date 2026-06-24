"""
Chat history management for AI conversations.
Stores and retrieves user conversation history from MongoDB.
"""

from datetime import datetime, timezone
from typing import Any
from database.connection import get_db
from config import CHAT_HISTORY_LIMIT


# ═══════════════════════════════════════════════════════
#  CHAT HISTORY — Collection: chat_histories
# ═══════════════════════════════════════════════════════

async def add_message(user_id: int, role: str, content: str) -> None:
    """
    Push a message to the user's chat history.
    Auto-trims to CHAT_HISTORY_LIMIT using $slice.
    
    Args:
        user_id: User's Telegram ID.
        role: Message role ("user" or "assistant").
        content: Message content text.
    """
    db = get_db()
    await db.chat_histories.update_one(
        {"user_id": user_id},
        {
            "$push": {
                "history": {
                    "$each": [{"role": role, "content": content}],
                    "$slice": -CHAT_HISTORY_LIMIT,
                }
            },
            "$set": {"updated_at": datetime.now(timezone.utc)},
            "$setOnInsert": {"user_id": user_id},
        },
        upsert=True,
    )


async def get_history(user_id: int) -> list[dict[str, Any]]:
    """
    Return the message history array for a user.
    
    Args:
        user_id: User's Telegram ID.
        
    Returns:
        List of message dictionaries with "role" and "content" keys, or [] if not found.
    """
    db = get_db()
    doc = await db.chat_histories.find_one({"user_id": user_id})
    if doc and "history" in doc:
        return doc["history"]
    return []


async def clear_history(user_id: int) -> None:
    """
    Delete a user's entire chat history document.
    
    Args:
        user_id: User's Telegram ID.
    """
    db = get_db()
    await db.chat_histories.delete_one({"user_id": user_id})
