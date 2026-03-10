import os
import logging
from pyrogram import Client
from pyrogram.enums import ChatAction

log = logging.getLogger("SenpaiBot")

# ──── Supported extensions ────
_IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
_VIDEO_EXTS = {".mp4", ".mov", ".webm"}


def detect_media_type(url: str) -> str:
    """Return 'photo', 'video', or 'unknown' based on URL extension."""
    if not url:
        return "unknown"
    ext = os.path.splitext(url.split("?")[0])[1].lower()
    if ext in _IMAGE_EXTS:
        return "photo"
    if ext in _VIDEO_EXTS:
        return "video"
    return "unknown"


async def send_media(client: Client, chat_id: int, media, caption: str = "", reply_markup=None):
    """
    Send media (single URL or list of URLs) with caption.
    Falls back to text-only on any error.
    """
    if not media:
        await client.send_message(chat_id, caption, reply_markup=reply_markup)
        return

    # Normalize to list
    urls = media if isinstance(media, list) else [media]

    sent = False
    for url in urls:
        try:
            media_type = detect_media_type(url)
            await client.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)

            if media_type == "photo":
                await client.send_photo(
                    chat_id, url,
                    caption=caption if not sent else "",
                    reply_markup=reply_markup if not sent else None,
                )
                sent = True
            elif media_type == "video":
                await client.send_chat_action(chat_id, ChatAction.UPLOAD_VIDEO)
                await client.send_video(
                    chat_id, url,
                    caption=caption if not sent else "",
                    reply_markup=reply_markup if not sent else None,
                )
                sent = True
            else:
                # Unknown type — try as photo first
                await client.send_photo(
                    chat_id, url,
                    caption=caption if not sent else "",
                    reply_markup=reply_markup if not sent else None,
                )
                sent = True
        except Exception as e:
            log.warning(f"Media send failed ({url}): {e}")
            continue

    # Fallback to text if no media sent successfully
    if not sent:
        await client.send_message(chat_id, caption, reply_markup=reply_markup)
