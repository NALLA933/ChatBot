import logging
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from config import (
    START_MEDIA, SEND_MEDIA_IN_GROUP,
    DM_WELCOME, GROUP_WELCOME, BOT_USERNAME,
)
from database.users import upsert_user
from utils.keyboards import main_keyboard, friends_keyboard
from utils.helpers import send_media

log = logging.getLogger("SenpaiBot")


# ═══════════════════════════════════════════════════════
#  /start — DM (Private Chat)
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.command("start") & filters.private, group=1)
async def start_dm(client: Client, message: Message):
    try:
        user = message.from_user
        if user:
            await upsert_user(user.id, user.username, user.first_name)

        kb = main_keyboard(BOT_USERNAME)

        if START_MEDIA:
            await send_media(
                client, message.chat.id,
                START_MEDIA,
                caption=DM_WELCOME,
                reply_markup=kb,
            )
        else:
            await message.reply(DM_WELCOME, reply_markup=kb)
    except Exception as e:
        log.error(f"start_dm error: {e}")
        await message.reply(DM_WELCOME, reply_markup=main_keyboard(BOT_USERNAME))


# ═══════════════════════════════════════════════════════
#  /start — Group Chat
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.command("start") & filters.group, group=1)
async def start_group(client: Client, message: Message):
    try:
        group_name = message.chat.title or "this group"
        text = GROUP_WELCOME.format(group_name=group_name)
        kb = main_keyboard(BOT_USERNAME)

        if START_MEDIA and SEND_MEDIA_IN_GROUP:
            await send_media(
                client, message.chat.id,
                START_MEDIA,
                caption=text,
                reply_markup=kb,
            )
        else:
            await message.reply(text, reply_markup=kb)
    except Exception as e:
        log.error(f"start_group error: {e}")


# ═══════════════════════════════════════════════════════
#  CALLBACK — Friends
# ═══════════════════════════════════════════════════════

@Client.on_callback_query(filters.regex("^cb_friends$"), group=1)
async def cb_friends(client: Client, callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "👥 **ꜰʀɪᴇɴᴅ ɢᴄꜱ**\n\nᴊᴏɪɴ ᴏᴜʀ ꜰʀɪᴇɴᴅ ɢʀᴏᴜᴘꜱ ʙᴇʟᴏᴡ! 👇",
            reply_markup=friends_keyboard(),
        )
        await callback.answer()
    except Exception as e:
        log.error(f"cb_friends error: {e}")
        await callback.answer("Something went wrong!", show_alert=True)


# ═══════════════════════════════════════════════════════
#  CALLBACK — Back to Main
# ═══════════════════════════════════════════════════════

@Client.on_callback_query(filters.regex("^cb_back_main$"), group=1)
async def cb_back_main(client: Client, callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            DM_WELCOME,
            reply_markup=main_keyboard(BOT_USERNAME),
        )
        await callback.answer()
    except Exception as e:
        log.error(f"cb_back_main error: {e}")
        await callback.answer("Something went wrong!", show_alert=True)
