import asyncio
import logging
import sys
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from database.connection import connect_db

# ──── Logging ────
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
# Only show SenpaiBot logs, silence everything else
log = logging.getLogger("SenpaiBot")
log.setLevel(logging.INFO)

# Silence noisy loggers
for noisy in ("pyrogram", "httpx", "httpcore", "motor", "pymongo"):
    logging.getLogger(noisy).setLevel(logging.ERROR)

# ──── Event loop fix for Windows + Python 3.10+ ────
if sys.platform == "win32" and sys.version_info >= (3, 10):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ──── Pyrogram Client ────
app = Client(
    name="senpai_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
)


async def main():
    # Pehle database connect karein
    await connect_db()
    log.info("MongoDB connected!")
    
    # Phir bot start karein
    await app.start()
    log.info("Senpai Bot is running!")
    
    # Bot ko background me active rakhne ke liye idle use karein
    await idle()  
    
    # Script stop hone par bot ko safely shutdown karein
    await app.stop()


if __name__ == "__main__":
    try:
        # Pura async process yahan se trigger hoga
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Bot stopped.")
