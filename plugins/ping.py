import time
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.smallcaps import sc


@Client.on_message(filters.command("ping"), group=1)
async def ping_handler(client: Client, message: Message):
    start = time.time()
    msg = await message.reply(sc("pinging..."))
    end = time.time()
    ms = round((end - start) * 1000)
    await msg.edit_text(f"🏓 **ᴘᴏɴɢ!**\n⚡ `{ms}ms`")
