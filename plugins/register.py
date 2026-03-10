import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database.users import upsert_user, upsert_group

log = logging.getLogger("SenpaiBot")


# ═══════════════════════════════════════════════════════
#  SILENT AUTO-REGISTRATION — DM
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.private & filters.incoming, group=0)
async def register_dm(client: Client, message: Message):
    """Silently register every DM user."""
    try:
        user = message.from_user
        if not user or user.is_bot:
            return
        await upsert_user(user.id, user.username, user.first_name)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
#  SILENT AUTO-REGISTRATION — GROUP (new_chat_members)
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.new_chat_members, group=0)
async def register_new_member(client: Client, message: Message):
    """When bot is added to group → register the group."""
    try:
        me = await client.get_me()
        for member in message.new_chat_members:
            if member.id == me.id:
                # Bot was added to this group
                chat = message.chat
                await upsert_group(chat.id, chat.title, chat.username)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
#  SILENT AUTO-REGISTRATION — GROUP (any message)
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.group & filters.incoming, group=0)
async def register_group_message(client: Client, message: Message):
    """Backup: register group + sender on any group message."""
    try:
        chat = message.chat
        await upsert_group(chat.id, chat.title, chat.username)

        user = message.from_user
        if user and not user.is_bot:
            await upsert_user(user.id, user.username, user.first_name)
    except Exception:
        pass
