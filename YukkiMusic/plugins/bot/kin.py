from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

@app.on_message(filters.regex("^مطور السورس$"))
def show_developer_info(client, message):
    developer_id = "1854384004"
    user = app.get_users(developer_id)

    bio = getattr(user, "bio", "No Bio")
    username = getattr(user, "username", "No Username")

    caption = f"Name: {user.first_name}\nID: {user.id}\nBio: {bio}\nUsername: @{username}"

    inline_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⦗ مطور السورس ⦘", url=f"https://t.me/{username}")]]
    )

    client.send_message(
        chat_id=message.chat.id, 
        text=caption,
        reply_markup=inline_keyboard  
    )
