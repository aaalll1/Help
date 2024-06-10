from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

@app.on_message(filters.regex("^مطور السورس$"))
async def show_developer_info(client, message):
    developer_id = "1854384004"
    user = await app.get_users(developer_id)

    if user:
        if user.photo:
            photo_file = await app.download_media(user.photo.big_file_id)
        else:
            photo_file = None

        # Check if bio exists, if not, use other available information
        bio = user.bio if hasattr(user, 'bio') else "No Bio"
        first_name = user.first_name if hasattr(user, 'first_name') else "No First Name"
        last_name = user.last_name if hasattr(user, 'last_name') else "No Last Name"
        username = f"@{user.username}" if hasattr(user, 'username') and user.username else "No Username"

        caption = f"First Name: {first_name}\nLast Name: {last_name}\nID: {user.id}\nBio: {bio}\nUsername: {username}"

        inline_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("⦗ مطور السورس ⦘", url=f"https://t.me/{username}")]]
        )

        # Send photo to the user who sent the command
        if photo_file:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo_file,
                caption=caption,
                reply_to_message_id=message["message_id"],  # Reply to the user's message
                reply_markup=inline_keyboard
            )
        else:
            await client.send_message(
                chat_id=message.chat.id,
                text=caption,
                reply_to_message_id=message["message_id"],  # Reply to the user's message
                reply_markup=inline_keyboard
            )
    else:
        await message.reply_text("Failed to fetch developer information.")
