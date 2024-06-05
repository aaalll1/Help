from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic.utils.formatters import time_to_seconds
from YukkiMusic import app
from strings.filters import command

# Function to get dynamic data
def get_dynamic_data(chat_id):
    # Replace with your logic to fetch data dynamically
    played = "Your played text"
    bar = "Your bar text"
    dur = "Your duration text"
    videoid = "Your video ID"
    return played, bar, dur, videoid, chat_id

@app.on_message(command("تحكم"))
async def derws(client, message):
    chat_id = message.chat.id
    played, bar, dur, videoid, chat_id = get_dynamic_data(chat_id)

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
        [InlineKeyboardButton(text="إغلاق القائمة", callback_data="close")],
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_text("قائمة التحكم:", reply_markup=reply_markup)
