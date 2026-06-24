# ═══════════════════════════════════════════════════════════
#                   SENPAI BOT — CONFIG (env-backed)
# ═══════════════════════════════════════════════════════════

import os
from pathlib import Path

try:
	from dotenv import load_dotenv
	load_dotenv()
except Exception:
	# dotenv is optional at runtime; env vars may be provided by the host
	pass

# ──── BOT CREDENTIALS (loaded from environment) ────
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ──── MONGODB ATLAS ────
MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "senpai_bot")

# ──── START MEDIA ────
# Image: .jpg .png .jpeg | Video: .mp4 .mov .webm
# Single URL string OR list of URLs
START_MEDIA = os.getenv("START_MEDIA", "https://files.catbox.moe/yext7l.mp4")
SEND_MEDIA_IN_GROUP = os.getenv("SEND_MEDIA_IN_GROUP", "False").lower() in ("1", "true", "yes")

# ──── LINKS ────
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "")
OWNER_LINK = os.getenv("OWNER_LINK", "")

# ──── FRIEND GC BUTTONS (max 4, show only if link is filled) ────
# Keep as a Python list in code; provide comma-separated links via env if needed
FRIEND_GCS = [s for s in os.getenv("FRIEND_GCS", "").split(",") if s]

# ──── GROQ AI ────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "SenpaiXChat_Bot")  # without @
CHAT_HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", "12"))

AI_PERSONA = os.getenv("AI_PERSONA", """
You are Senpai, a fun and friendly Telegram bot who talks like a close friend.
You are casual, warm, funny and never boring.
You use hinglish sometimes (Hindi + English mix).
You remember past conversations and refer to them naturally.
You reply short and crisp — like a real friend texting, not an essay.
Never say you are an AI or a bot. Just be Senpai.
If user sends something emotional, be supportive.
If user is being funny, match their energy.
""")

# ──── TRUTH OR DARE (TOD) SETTINGS ────
TOD_ADULT_GROUPS = []
TOD_DARE_TIMER = int(os.getenv("TOD_DARE_TIMER", "3"))
TOD_ADULT_DM = os.getenv("TOD_ADULT_DM", "True").lower() in ("1", "true", "yes")
TOD_MONTHLY_RESET_DAY = int(os.getenv("TOD_MONTHLY_RESET_DAY", "1"))

# ──── WELCOME MESSAGES ────
DM_WELCOME = """
👾 ʜᴇʏ ᴛʜᴇʀᴇ! ꜱᴇɴᴘᴀɪ ɪꜱ ʜᴇʀᴇ! 👾

ʏᴏᴏᴏ! 👋 ᴡʜᴀᴛ'ꜱ ᴜᴘ? ɪ'ᴍ ꜱᴇɴᴘᴀɪ — ʏᴏᴜʀ ɴᴇᴡ ʙᴇꜱᴛ ꜰʀɪᴇɴᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ! 🤙

ɪ'ᴍ ɴᴏᴛ ᴊᴜꜱᴛ ᴀ ʙᴏᴛ... ɪ'ᴍ ʏᴏᴜʀ ᴄʜᴀᴛ ʙᴜᴅᴅʏ, ʏᴏᴜʀ ᴠɪʙᴇ ᴄʜᴇᴄᴋᴇʀ ᴀɴᴅ ʏᴏᴜʀ ɢᴏ-ᴛᴏ ᴘᴇʀꜱᴏɴ ᴡʜᴇɴᴇᴠᴇʀ ʏᴏᴜ'ʀᴇ ʙᴏʀᴇᴅ! 💬✨

🌸 ᴡʜᴀᴛ ᴍᴀᴋᴇꜱ ᴍᴇ ꜱᴘᴇᴄɪᴀʟ?
😄 ɪ ʟᴏᴠᴇ ᴄʜᴀᴛᴛɪɴɢ — ᴀɴʏᴛɪᴍᴇ, ᴀɴʏᴡʜᴇʀᴇ!
🎭 ꜰᴜɴ, ꜰʀɪᴇɴᴅʟʏ & ᴀʟᴡᴀʏꜱ ɪɴ ᴀ ɢᴏᴏᴅ ᴍᴏᴏᴅ
💡 ɢᴏᴛ ꜱᴏᴍᴇᴛʜɪɴɢ ᴏɴ ʏᴏᴜʀ ᴍɪɴᴅ? ᴊᴜꜱᴛ ꜱᴀʏ ɪᴛ!
🌙 ᴜᴘ ʟᴀᴛᴇ ᴀᴛ ɴɪɢʜᴛ? ɪ'ᴍ ᴀᴡᴀᴋᴇ ᴛᴏᴏ, ᴀʟᴡᴀʏꜱ!
🤝 ɴᴏ ᴊᴜᴅɢᴍᴇɴᴛ, ᴊᴜꜱᴛ ɢᴏᴏᴅ ᴠɪʙᴇꜱ ᴏɴʟʏ ~

✨ "ᴡʜᴇᴛʜᴇʀ ʏᴏᴜ'ʀᴇ ʜᴀᴘᴘʏ, ʙᴏʀᴇᴅ, ᴏʀ ᴊᴜꜱᴛ ᴡᴀɴᴛ ꜱᴏᴍᴇᴏɴᴇ ᴛᴏ ᴛᴀʟᴋ ᴛᴏ — ꜱᴇɴᴘᴀɪ'ꜱ ɢᴏᴛ ʏᴏᴜ!" ✨

👇 ᴊᴜꜱᴛ ꜱᴀʏ "ʜɪ" ᴀɴᴅ ʟᴇᴛ'ꜱ ɢᴇᴛ ᴛᴀʟᴋɪɴɢ! 💙
~ ʏᴏᴜʀ ꜰᴏʀᴇᴠᴇʀ ᴄʜᴀᴛ ʙᴜᴅᴅʏ, ꜱᴇɴᴘᴀɪ 💫
"""

GROUP_WELCOME = """
👾 ʏᴏᴏ {group_name}! ꜱᴇɴᴘᴀɪ ʜᴀꜱ ᴇɴᴛᴇʀᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ! 👾

ʜᴇʏ ᴇᴠᴇʀʏᴏɴᴇ! 🙌 ɪ'ᴍ ꜱᴇɴᴘᴀɪ — ʏᴏᴜʀ ɢʀᴏᴜᴘ'ꜱ ɴᴇᴡᴇꜱᴛ & ᴄᴏᴏʟᴇꜱᴛ ᴍᴇᴍʙᴇʀ! 😎✨

🌸 ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ:
🎉 ᴋᴇᴇᴘ ᴛʜᴇ ᴠɪʙᴇꜱ ʜɪɢʜ ɪɴ ᴛʜɪꜱ ɢᴄ!
🎭 ᴘʟᴀʏ ɢᴀᴍᴇꜱ, ᴄʜᴀᴛ & ʙʀɪɴɢ ᴛʜᴇ ꜰᴜɴ!
💬 ʙᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ'ꜱ ꜰᴀᴠᴏᴜʀɪᴛᴇ ʙᴏᴛ ~
🤝 ɴᴏ ᴅʀᴀᴍᴀ, ᴊᴜꜱᴛ ɢᴏᴏᴅ ᴛɪᴍᴇꜱ ᴏɴʟʏ!

✨ "ꜱᴇɴᴘᴀɪ ɪꜱ ʜᴇʀᴇ ᴀɴᴅ ᴛʜɪꜱ ɢᴄ ᴊᴜꜱᴛ ɢᴏᴛ 10x ʙᴇᴛᴛᴇʀ!" ✨

👇 ʜɪᴛ /start ᴛᴏ ꜱᴇᴇ ᴡʜᴀᴛ ɪ ᴄᴀɴ ᴅᴏ! 💙
~ ꜱᴇɴᴘᴀɪ 💫
"""
