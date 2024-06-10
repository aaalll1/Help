from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

def get_user_info(user_id):
    user = app.get_users(user_id)
    bio = user.bio if hasattr(user, "bio") else "No Bio"
    birthdate = user.birthdate if hasattr(user, "birthdate") else "No Birthdate"
    return {
        "name": user.first_name if user.first_name else "No Name",
        "id": user.id,
        "bio": bio,
        "birthdate": birthdate,
        "photo": user.photo.big_file_id if user.photo else None
    }

@app.on_message(filters.regex("^مطور السورس$"))
def show_developer_info(client, message):
    # Developer ID (Replace with actual developer ID)
    developer_id = "1854384004"
    developer_info = get_user_info(developer_id)
    inline_button = InlineKeyboardButton("⦗ مطور السورس ⦘", url="https://t.me/RR8R9")

    inline_markup = InlineKeyboardMarkup([[inline_button]])

    client.send_photo(
        chat_id=message.chat.id,
        photo=developer_info["photo"],
        caption=f"Name: {developer_info['name']}\nID: {developer_info['id']}\nBio: {developer_info['bio']}\nBirthdate: {developer_info['birthdate']}",
        reply_markup=inline_markup
    )
