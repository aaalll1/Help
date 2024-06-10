from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

@app.on_message(filters.regex("^مطور السورس$"))
def show_developer_info(client, message):
    developer_id = "1854384004"
    user = app.get_users(developer_id)

    if user.photo:
        photo_file = app.download_media(user.photo.big_file_id)
    else:
        photo_file = None

    # Check if bio exists, if so, copy it
    bio = user.stringify() if user.bio else "No Bio"

    username = f"@{user.username}" if user.username else "No Username"

    caption = f"Name: {user.first_name}\nID: {user.id}\nBio: {bio}\nUsername: {username}"

    inline_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⦗ ожидании ⦘", url=f"https://t.me/{username}")]]
    )

    # Send photo to the user who sent the command
    if photo_file:
        client.send_photo(
            chat_id=message.chat.id,
            photo=photo_file,
            caption=caption,
            reply_to_message_id=message.message_id,  # Reply to the user's message
            reply_markup=inline_keyboard
        )
    else:
        client.send_message(
            chat_id=message.chat.id,
            text=caption,
            reply_to_message_id=message.message_id,  # Reply to the user's message
            reply_markup=inline_keyboard
        )
