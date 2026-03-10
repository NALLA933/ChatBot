import re
import random
import asyncio
import logging
from groq import Groq
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from config import (
    GROQ_API_KEY, GROQ_MODEL, BOT_USERNAME,
    BOT_STICKER_PACK, AI_PERSONA, OWNER_ID,
)
from database.chat_history import add_message, get_history, clear_history
from utils.sticker_helper import (
    save_user_sticker_pack, get_user_sticker,
    get_bot_sticker, save_bot_pack,
)
from utils.smallcaps import sc

log = logging.getLogger("SenpaiBot")

# ──── Groq client (module-level, once) ────
groq_client = Groq(api_key=GROQ_API_KEY)


# ═══════════════════════════════════════════════════════
#  AI REPLY LOGIC
# ═══════════════════════════════════════════════════════

async def get_ai_reply(user_id: int, user_message: str) -> str:
    """Get AI reply from Groq with conversation memory."""
    history = await get_history(user_id)

    messages = [{"role": "system", "content": AI_PERSONA}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        response = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=300,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()

        if not reply:
            return sc("hmm... senpai got confused, say that again?")

        # Save to history
        await add_message(user_id, "user", user_message)
        await add_message(user_id, "assistant", reply)
        return reply

    except Exception as e:
        if "rate_limit" in str(e).lower():
            await asyncio.sleep(5)
            try:
                response = await asyncio.to_thread(
                    groq_client.chat.completions.create,
                    model=GROQ_MODEL,
                    messages=messages,
                    max_tokens=300,
                    temperature=0.85,
                )
                reply = response.choices[0].message.content.strip()
                if reply:
                    await add_message(user_id, "user", user_message)
                    await add_message(user_id, "assistant", reply)
                    return reply
            except Exception:
                pass

        # Timeout / other → retry once after 2s
        log.warning(f"Groq error: {e}")
        await asyncio.sleep(2)
        try:
            response = await asyncio.to_thread(
                groq_client.chat.completions.create,
                model=GROQ_MODEL,
                messages=messages,
                max_tokens=300,
                temperature=0.85,
            )
            reply = response.choices[0].message.content.strip()
            if reply:
                await add_message(user_id, "user", user_message)
                await add_message(user_id, "assistant", reply)
                return reply
        except Exception:
            pass

        return sc("senpai is thinking... try again!")


# ═══════════════════════════════════════════════════════
#  STICKER LOGIC
# ═══════════════════════════════════════════════════════

async def maybe_send_sticker(client: Client, message: Message, user_id: int) -> bool:
    """Maybe send a sticker reply. Return True if sticker was sent."""
    try:
        if message.sticker:
            # User sent a sticker → 60% chance reply with sticker
            if random.random() < 0.60:
                # Try user pack first, fallback to bot pack
                file_id = await get_user_sticker(user_id)
                if not file_id:
                    file_id = await get_bot_sticker()
                if file_id:
                    await message.reply_sticker(file_id)
                    return True
        else:
            # Normal message → 15% chance send from bot pack
            if random.random() < 0.15:
                file_id = await get_bot_sticker()
                if file_id:
                    await message.reply_sticker(file_id)
                    return True
    except Exception as e:
        log.warning(f"Sticker send error: {e}")
    return False


def _clean_message(text: str) -> str:
    """Strip bot username and 'senpai' keyword from message before AI."""
    if not text:
        return ""
    text = re.sub(rf"@{re.escape(BOT_USERNAME)}", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bsenpai\b", "", text, flags=re.IGNORECASE)
    return text.strip()


# ═══════════════════════════════════════════════════════
#  STICKER HANDLER — Save user sticker packs
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.sticker & filters.private, group=5)
async def sticker_handler_dm(client: Client, message: Message):
    """When user sends sticker in DM → save pack + maybe reply."""
    try:
        user = message.from_user
        if not user or user.is_bot:
            return

        # Save sticker pack
        sticker = message.sticker
        if sticker and sticker.set_name:
            try:
                sticker_set = await client.get_sticker_set(sticker.set_name)
                file_ids = [s.file_id for s in sticker_set.stickers]
                await save_user_sticker_pack(user.id, sticker.set_name, file_ids)
            except Exception:
                pass

        # Maybe reply with sticker
        sticker_sent = await maybe_send_sticker(client, message, user.id)

        # Also reply with AI text sometimes
        if random.random() < 0.5:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            reply = await get_ai_reply(user.id, "(user sent a sticker)")
            await message.reply(reply)

    except Exception as e:
        log.error(f"sticker_handler_dm error: {e}")


@Client.on_message(filters.sticker & filters.group, group=5)
async def sticker_handler_group(client: Client, message: Message):
    """When user sends sticker in group → save pack silently."""
    try:
        user = message.from_user
        if not user or user.is_bot:
            return
        sticker = message.sticker
        if sticker and sticker.set_name:
            try:
                sticker_set = await client.get_sticker_set(sticker.set_name)
                file_ids = [s.file_id for s in sticker_set.stickers]
                await save_user_sticker_pack(user.id, sticker.set_name, file_ids)
            except Exception:
                pass
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
#  AI CHAT — DM (Private)
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.private & filters.incoming & ~filters.command(["start", "reset", "broadcast", "loadstickers"]) & ~filters.sticker, group=10)
async def ai_chat_dm(client: Client, message: Message):
    """Every incoming DM message → AI reply."""
    try:
        user = message.from_user
        if not user or user.is_bot:
            return

        text = message.text or message.caption or ""
        if not text.strip():
            return

        # Maybe send a sticker first
        await maybe_send_sticker(client, message, user.id)

        # AI reply
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        cleaned = _clean_message(text)
        reply = await get_ai_reply(user.id, cleaned)
        await message.reply(reply)

    except Exception as e:
        log.error(f"ai_chat_dm error: {e}")


# ═══════════════════════════════════════════════════════
#  AI CHAT — Group
# ═══════════════════════════════════════════════════════

def _should_reply_in_group(client_id: int, message: Message) -> bool:
    """Check if bot should reply in group."""
    text = (message.text or message.caption or "").lower()

    # Trigger 1: text contains "senpai"
    if "senpai" in text:
        return True

    # Trigger 2: text contains @BOT_USERNAME
    if f"@{BOT_USERNAME.lower()}" in text:
        return True

    # Trigger 3: reply to bot's own message
    if message.reply_to_message and message.reply_to_message.from_user:
        if message.reply_to_message.from_user.id == client_id:
            return True

    return False


@Client.on_message(filters.group & filters.incoming & ~filters.command(["start", "broadcast"]) & ~filters.sticker, group=10)
async def ai_chat_group(client: Client, message: Message):
    """Reply in group only when triggered by keyword/mention/reply."""
    try:
        user = message.from_user
        if not user or user.is_bot:
            return

        me = await client.get_me()
        if not _should_reply_in_group(me.id, message):
            return

        text = message.text or message.caption or ""
        if not text.strip():
            return

        # Maybe send sticker
        await maybe_send_sticker(client, message, user.id)

        # AI reply
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        cleaned = _clean_message(text)
        reply = await get_ai_reply(user.id, cleaned)
        await message.reply(reply)

    except Exception as e:
        log.error(f"ai_chat_group error: {e}")


# ═══════════════════════════════════════════════════════
#  /reset — Clear chat memory (DM only)
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.command("reset") & filters.private, group=3)
async def reset_handler(client: Client, message: Message):
    try:
        user = message.from_user
        if not user:
            return
        await clear_history(user.id)
        await message.reply(sc("memory cleared! fresh start senpai mode on"))
    except Exception as e:
        log.error(f"reset error: {e}")


# ═══════════════════════════════════════════════════════
#  /loadstickers — Owner only
# ═══════════════════════════════════════════════════════

@Client.on_message(filters.command("loadstickers") & filters.private, group=3)
async def loadstickers_handler(client: Client, message: Message):
    try:
        user = message.from_user
        if not user or user.id != int(OWNER_ID):
            return await message.reply(sc("you are not allowed to use this command"))

        sticker_set = await client.get_sticker_set(BOT_STICKER_PACK)
        file_ids = [s.file_id for s in sticker_set.stickers]
        await save_bot_pack(file_ids)
        await message.reply(sc(f"loaded {len(file_ids)} stickers from {BOT_STICKER_PACK}"))

    except Exception as e:
        log.error(f"loadstickers error: {e}")
        await message.reply(sc("failed to load sticker pack! check pack name."))
