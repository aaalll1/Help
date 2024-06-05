from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic.utils.formatters import time_to_seconds
from YukkiMusic import app
from strings.filters import command

@app.on_message(command("تحكم"))
async def derws(client, message):
    chat_id = message.chat.id

    buttons = [
        [
            InlineKeyboardButton(
                text="⦗ Resume ⦘",
                callback_data=f"ADMIN Resume|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⦗ Pause ⦘",
                callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⦗ Skip ⦘",
                callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⦗ Stop ⦘",
                callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⦗ Mute ⦘",
                callback_data=f"ADMIN Mute|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⦗ Unmute ⦘",
                callback_data=f"ADMIN Unmute|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="إغلاق القائمة",
                callback_data="close"
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_text("قائمة التحكم:", reply_markup=reply_markup)
