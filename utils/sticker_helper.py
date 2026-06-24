"""
Sticker pack management and retrieval utilities.
Stores user sticker packs in MongoDB with auto-expiration.
"""

import random
import logging
from datetime import datetime, timezone
from typing import Optional
from database.connection import get_db

log = logging.getLogger("SenpaiBot")


# ═══════════════════════════════════════════════════════
#  STICKER PACK MANAGEMENT — Collection: sticker_packs
#  Only user sticker packs (no bot pack)
#  TTL: auto-expire after 7 days of inactivity
# ═══════════════════════════════════════════════════════

async def ensure_sticker_indexes() -> None:
    """
    Create TTL index on sticker_packs collection (call once on startup).
    Auto-expires documents 7 days after last update.
    """
    db = get_db()
    await db.sticker_packs.create_index(
        "saved_at",
        expireAfterSeconds=604800,  # 7 days
    )


async def save_user_sticker_pack(
    user_id: int,
    pack_name: str,
    file_ids: list[str]
) -> None:
    """
    Upsert a sticker pack for a user. TTL resets on every save.
    
    Args:
        user_id: User's Telegram ID.
        pack_name: Name of the sticker pack.
        file_ids: List of sticker file IDs in the pack.
    """
    db = get_db()
    await db.sticker_packs.update_one(
        {"user_id": user_id, "pack_name": pack_name},
        {
            "$set": {
                "user_id": user_id,
                "pack_name": pack_name,
                "file_ids": file_ids,
                "saved_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )


async def get_user_sticker(user_id: int) -> Optional[str]:
    """
    Return a random sticker file_id from user's most recently used pack.
    Sort by saved_at desc → pick latest pack → random sticker from it.
    
    Args:
        user_id: User's Telegram ID.
        
    Returns:
        Random sticker file_id from the most recent pack, or None if no packs exist.
    """
    db = get_db()
    packs = await (
        db.sticker_packs
        .find({"user_id": user_id})
        .sort("saved_at", -1)
        .to_list(length=1)
    )
    if not packs:
        return None
    file_ids = packs[0].get("file_ids", [])
    if not file_ids:
        return None
    return random.choice(file_ids)


async def has_user_stickers(user_id: int) -> bool:
    """
    Check if user has any saved sticker pack.
    
    Args:
        user_id: User's Telegram ID.
        
    Returns:
        True if user has at least one saved sticker pack.
    """
    db = get_db()
    doc = await db.sticker_packs.find_one({"user_id": user_id}, {"_id": 1})
    return doc is not None
