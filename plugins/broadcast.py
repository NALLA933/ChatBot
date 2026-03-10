import os
import json
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserIsBlocked, ChatWriteForbidden, FloodWait
from config import OWNER_ID
from database.users import get_all_users, get_all_groups
from data.strings import (
    BROADCAST_USAGE, BROADCAST_STARTED, BROADCAST_DONE,
    BROADCAST_GROUPS_DONE, BROADCAST_NO_USERS, BROADCAST_NO_GROUPS,
    BROADCAST_FAIL_REPORT, NO_PERMISSION,
)

log = logging.getLogger("SenpaiBot")


def _is_owner(user_id: int) -> bool:
    """Check if user is the bot owner (support int and string)."""
    return user_id == int(OWNER_ID)


async def _copy_with_retry(client: Client, message: Message, chat_id: int) -> bool:
    """Copy message to a chat. Handle FloodWait with one retry."""
    try:
        await client.copy_message(
            chat_id=chat_id,
            from_chat_id=message.chat.id,
            message_id=message.id,
        )
        return True
    except FloodWait as e:
        await asyncio.sleep(e.value)
        try:
            await client.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.id,
            )
            return True
        except Exception:
            return False
    except (UserIsBlocked, ChatWriteForbidden):
        return False
    except Exception as e:
        log.warning(f"Broadcast copy failed for {chat_id}: {e}")
        return False


async def _send_failed_report(client: Client, chat_id: int, report: dict):
    """Write failed report JSON to /tmp, send as document, then delete."""
    path = "/tmp/failed_report.json"
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        await client.send_document(chat_id, path, caption=BROADCAST_FAIL_REPORT)
    except Exception as e:
        log.error(f"Failed report send error: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)


# ═══════════════════════════════════════════════════════
#  /broadcast  — Groups only
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.command("broadcast") & filters.private & ~filters.regex(r"-user"), group=2)
async def broadcast_groups(client: Client, message: Message):
    user = message.from_user
    if not user or not _is_owner(user.id):
        return await message.reply(NO_PERMISSION)

    if not message.reply_to_message:
        return await message.reply(BROADCAST_USAGE)

    groups = await get_all_groups()
    if not groups:
        return await message.reply(BROADCAST_NO_GROUPS)

    await message.reply(BROADCAST_STARTED)

    success = 0
    failed_ids = []

    for i, group in enumerate(groups):
        ok = await _copy_with_retry(client, message.reply_to_message, group["chat_id"])
        if ok:
            success += 1
        else:
            failed_ids.append(group["chat_id"])

        # Rate limit: sleep 1s every 25 messages
        if (i + 1) % 25 == 0:
            await asyncio.sleep(1)

    failed = len(failed_ids)
    await message.reply(f"{BROADCAST_GROUPS_DONE}\n\n✅ ꜱᴜᴄᴄᴇꜱꜱ: {success} | ❌ ꜰᴀɪʟᴇᴅ: {failed}")

    if failed > 0:
        report = {
            "total_groups": len(groups),
            "success": success,
            "failed": failed,
            "failed_chat_ids": failed_ids,
        }
        await _send_failed_report(client, message.chat.id, report)


# ═══════════════════════════════════════════════════════
#  /broadcast -user  — Users + Groups
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.command("broadcast") & filters.private & filters.regex(r"-user"), group=2)
async def broadcast_users(client: Client, message: Message):
    user = message.from_user
    if not user or not _is_owner(user.id):
        return await message.reply(NO_PERMISSION)

    if not message.reply_to_message:
        return await message.reply(BROADCAST_USAGE)

    users = await get_all_users()
    groups = await get_all_groups()

    if not users and not groups:
        return await message.reply(BROADCAST_NO_USERS)

    await message.reply(BROADCAST_STARTED)

    # ── Users ──
    u_success, u_failed_ids = 0, []
    for i, u in enumerate(users):
        ok = await _copy_with_retry(client, message.reply_to_message, u["user_id"])
        if ok:
            u_success += 1
        else:
            u_failed_ids.append(u["user_id"])
        if (i + 1) % 25 == 0:
            await asyncio.sleep(1)

    # ── Groups ──
    g_success, g_failed_ids = 0, []
    for i, g in enumerate(groups):
        ok = await _copy_with_retry(client, message.reply_to_message, g["chat_id"])
        if ok:
            g_success += 1
        else:
            g_failed_ids.append(g["chat_id"])
        if (i + 1) % 25 == 0:
            await asyncio.sleep(1)

    stats = (
        f"{BROADCAST_DONE}\n\n"
        f"👤 ᴜꜱᴇʀꜱ: ✅ {u_success} | ❌ {len(u_failed_ids)}\n"
        f"👥 ɢʀᴏᴜᴘꜱ: ✅ {g_success} | ❌ {len(g_failed_ids)}"
    )
    await message.reply(stats)

    total_failed = len(u_failed_ids) + len(g_failed_ids)
    if total_failed > 0:
        report = {
            "broadcast_type": "user+group",
            "users": {
                "total": len(users),
                "success": u_success,
                "failed": len(u_failed_ids),
                "failed_ids": u_failed_ids,
            },
            "groups": {
                "total": len(groups),
                "success": g_success,
                "failed": len(g_failed_ids),
                "failed_ids": g_failed_ids,
            },
        }
        await _send_failed_report(client, message.chat.id, report)
