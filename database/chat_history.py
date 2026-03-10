from datetime import datetime, timezone
from database.connection import get_db
from config import CHAT_HISTORY_LIMIT


# ═══════════════════════════════════════════════════════
#  CHAT HISTORY — Collection: chat_histories
# ═══════════════════════════════════════════════════════

async def add_message(user_id: int, role: str, content: str):
    """
    Push a message to the user's chat history.
    Auto-trims to CHAT_HISTORY_LIMIT using $slice.
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


async def get_history(user_id: int) -> list:
    """Return the message history array, or [] if not found."""
    db = get_db()
    doc = await db.chat_histories.find_one({"user_id": user_id})
    if doc and "history" in doc:
        return doc["history"]
    return []


async def clear_history(user_id: int):
    """Delete a user's entire chat history document."""
    db = get_db()
    await db.chat_histories.delete_one({"user_id": user_id})
