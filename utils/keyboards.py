from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT_GROUP, CHANNEL_LINK, OWNER_LINK, FRIEND_GCS


def main_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    """Main /start inline keyboard."""
    buttons = [
        # Row 1
        [InlineKeyboardButton(
            "👾 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 👾",
            url=f"https://t.me/{bot_username}?startgroup=true",
        )],
        # Row 2
        [
            InlineKeyboardButton("🫂 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url=SUPPORT_GROUP),
            InlineKeyboardButton("📢 ᴄʜᴀɴɴᴇʟ", url=CHANNEL_LINK),
        ],
        # Row 3
        [
            InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url=OWNER_LINK),
            InlineKeyboardButton("👥 ꜰʀɪᴇɴᴅꜱ", callback_data="cb_friends"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def friends_keyboard() -> InlineKeyboardMarkup:
    """Friends GC buttons — only show GCs that have a link filled."""
    buttons = []
    for gc in FRIEND_GCS:
        if gc.get("link"):
            buttons.append(
                [InlineKeyboardButton(gc["name"], url=gc["link"])]
            )
    # Back button
    buttons.append(
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="cb_back_main")]
    )
    return InlineKeyboardMarkup(buttons)
