from datetime import datetime, timezone
from database.connection import get_db


# ═══════════════════════════════════════════════════════
#  USERS COLLECTION
# ═══════════════════════════════════════════════════════

async def upsert_user(user_id: int, username: str = None, first_name: str = None):
    """Insert or update a user in the users collection."""
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


async def get_user(user_id: int) -> dict:
    """Get a single user document."""
    db = get_db()
    return await db.users.find_one({"user_id": user_id})


async def get_all_users() -> list:
    """Return all users from users collection."""
    db = get_db()
    return await db.users.find().to_list(length=None)


async def get_total_users() -> int:
    """Count total users."""
    db = get_db()
    return await db.users.count_documents({})


# ═══════════════════════════════════════════════════════
#  GROUPS COLLECTION (separate from users!)
# ═══════════════════════════════════════════════════════

async def upsert_group(chat_id: int, chat_title: str = None, username: str = None):
    """Insert or update a group in the groups collection."""
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


async def get_all_groups() -> list:
    """Return all groups from groups collection."""
    db = get_db()
    return await db.groups.find().to_list(length=None)


async def get_total_groups() -> int:
    """Count total groups."""
    db = get_db()
    return await db.groups.count_documents({})
