import asyncio
import logging
import sys
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from database.connection import connect_db

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log = logging.getLogger("SenpaiBot")
log.setLevel(logging.INFO)

for noisy in ("pyrogram", "httpx", "httpcore", "motor", "pymongo"):
    logging.getLogger(noisy).setLevel(logging.ERROR)

if sys.platform == "win32" and sys.version_info >= (3, 10):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Client(
    name="senpai_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
)

async def main():
    await connect_db()
    log.info("MongoDB connected!")
    
    await app.start()
    log.info("Senpai Bot is running!")
    
    await idle()
    
    await app.stop()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        log.info("Bot stopped.")
