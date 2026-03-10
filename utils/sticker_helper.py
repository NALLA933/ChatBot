import random
import logging
from datetime import datetime, timezone
from database.connection import get_db

log = logging.getLogger("SenpaiBot")


# ═══════════════════════════════════════════════════════
#  STICKER PACK MANAGEMENT — Collection: sticker_packs
# ═══════════════════════════════════════════════════════

async def save_user_sticker_pack(user_id: int, pack_name: str, file_ids: list):
    """Upsert a sticker pack for a user."""
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


async def get_user_sticker(user_id: int) -> str | None:
    """
    Return a random sticker file_id from a user's saved packs.
    Multiple packs → pick random pack → pick random sticker.
    """
    db = get_db()
    packs = await db.sticker_packs.find({"user_id": user_id}).to_list(length=None)
    if not packs:
        return None
    pack = random.choice(packs)
    file_ids = pack.get("file_ids", [])
    if not file_ids:
        return None
    return random.choice(file_ids)


async def get_bot_sticker() -> str | None:
    """Return a random sticker from the bot's own pack (user_id=0)."""
    db = get_db()
    pack = await db.sticker_packs.find_one({"user_id": 0})
    if not pack:
        return None
    file_ids = pack.get("file_ids", [])
    if not file_ids:
        return None
    return random.choice(file_ids)


async def save_bot_pack(file_ids: list):
    """Save the bot's own sticker pack (user_id=0)."""
    db = get_db()
    await db.sticker_packs.update_one(
        {"user_id": 0},
        {
            "$set": {
                "user_id": 0,
                "pack_name": "bot_pack",
                "file_ids": file_ids,
                "saved_at": datetime.now(timezone.utc),
            },
        },
        upsert=True,
    )
