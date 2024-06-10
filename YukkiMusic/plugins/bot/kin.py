from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

@app.on_message(filters.regex("^مطور السورس$"))
def show_developer_info(client, message):
    # Developer ID (Replace with actual developer ID)
    developer_id = "1854384004"
    user = app.get_users(developer_id)

    if user.photo:
        photo_file = app.download_media(user.photo.big_file_id)
    else:
        photo_file = None

    bio = getattr(user, "bio", "No Bio")

    caption = f"Name: {user.first_name}\nID: {user.id}\nBio: {bio}"

    # Send photo to the user who sent "مطور السورس"
    if photo_file:
        client.send_photo(
            chat_id=message.from_user.id,
            photo=photo_file,
            caption=caption
        )
    else:
        client.send_message(
            chat_id=message.from_user.id,
            text=caption
        )
