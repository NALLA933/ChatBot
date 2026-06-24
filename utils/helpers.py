"""
Helper utilities for media handling and chat actions.
"""

import os
import logging
from typing import Optional
from pyrogram import Client
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup

log = logging.getLogger("SenpaiBot")

# ──── Supported extensions ────
_IMAGE_EXTS: set[str] = {".jpg", ".jpeg", ".png"}
_VIDEO_EXTS: set[str] = {".mp4", ".mov", ".webm"}


def detect_media_type(url: str) -> str:
    """
    Detect media type based on URL extension.
    
    Args:
        url: URL string to analyze.
        
    Returns:
        "photo", "video", or "unknown" based on file extension.
    """
    if not url:
        return "unknown"
    ext = os.path.splitext(url.split("?")[0])[1].lower()
    if ext in _IMAGE_EXTS:
        return "photo"
    if ext in _VIDEO_EXTS:
        return "video"
    return "unknown"


async def send_media(
    client: Client,
    chat_id: int,
    media: Optional[str | list[str]],
    caption: str = "",
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> None:
    """
    Send media (single URL or list of URLs) with caption.
    Falls back to text-only on any error.
    
    Args:
        client: Pyrogram client instance.
        chat_id: Target chat ID.
        media: Single URL string or list of URLs (or None).
        caption: Caption text for the media.
        reply_markup: Optional inline keyboard markup.
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
