from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import math
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic.utils.formatters import time_to_seconds
from YukkiMusic import app

@app.on_message(command("تحكم"))
async def stream_markup_timer(client, message):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} •{bar}• {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text="✚ ᴘʟᴀʏʟɪsᴛ ✚", callback_data=f"add_playlist {videoid}"
            ),
        ],
        [
            InlineKeyboardButton(text="", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="⦗ تخطي ⦘", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="⦗ كتم ⦘", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton(
                text="⦗ إلغاء كتم ⦘", callback_data=f"ADMIN Unmute|{chat_id}"
            ),
        ],
        [InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")],
    ]
    return buttons

    # إنشاء InlineKeyboardMarkup
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_text("قائمة التحكم:", reply_markup=reply_markup)
