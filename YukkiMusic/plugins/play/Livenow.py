from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.errors import ChatAdminRequired
from YukkiMusic import app
from strings.filters import command

# Dictionary to store TV channels and their corresponding m3u8 URLs
TV_CHANNELS = {
    "قناة 1": "http://ns8.indexforce.com:1935/home/mystream1/chunklist_w921666703.m3u8",
    "قناة 2": "http://ns8.indexforce.com:1935/home/mystream1/chunklist_w921666703.m3u8",
    "قناة 3": "http://ns8.indexforce.com:1935/home/mystream1/chunklist_w921666703.m3u8",
    "قناة 4": "http://ns8.indexforce.com:1935/home/mystream1/chunklist_w921666703.m3u8",
    "قناة 5": "http://ns8.indexforce.com:1935/home/mystream1/chunklist_w921666703.m3u8",
}

# Command handler
@app.on_message(command(["قنوات التلفزيون"]) & filters.group)
async def tv_channels_command(client, message: Message):
    # Check if the user is admin in the chat
    try:
        await client.get_chat_member(message.chat.id, message.from_user.id)
    except ChatAdminRequired:
        await message.reply_text("يجب أن تكون مسؤولًا في المجموعة لاستخدام هذا الأمر.")
        return
    
    # Create inline keyboard with buttons for each TV channel
    keyboard = []
    row = []
    for channel_name, channel_url in TV_CHANNELS.items():
        row.append(InlineKeyboardButton(channel_name, callback_data=f"play_tv_{channel_name}"))
        if len(row) == 2:  # 2 buttons per row (you can change this number)
            keyboard.append(row)
            row = []
    
    # Add the last row if it's not empty
    if row:
        keyboard.append(row)
    
    # Create InlineKeyboardMarkup from the keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send message with inline keyboard
    await message.reply_text("اختر قناة التلفزيون للبث المباشر:", reply_markup=reply_markup)

# Callback query handler for playing the stream of selected TV channel
@app.on_callback_query(filters.regex("^play_tv_"))
async def play_tv_callback(client, callback_query: CallbackQuery):
    # Check if the user is admin in the chat
    try:
        await client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
    except ChatAdminRequired:
        await callback_query.answer("يجب أن تكون مسؤولًا في المجموعة لاستخدام هذا الأمر.", show_alert=True)
        return
    
    # Parse the callback data to get the channel name
    channel_name = callback_query.data.split("_", 1)[1]
    
    # Reply to callback query
    await callback_query.answer()
    
    # Start streaming the m3u8 link of the selected channel
    stream_url = TV_CHANNELS.get(channel_name)
    if stream_url:
        try:
            await callback_query.message.edit_text(f"جاري تشغيل قناة {channel_name}...")
            # Perform the streaming action here (using the provided code for streaming)
            await stream(client, callback_query.message, stream_url)
        except Exception as e:
            print(f"Error while streaming {channel_name}: {str(e)}")
            await callback_query.message.reply_text(f"حدث خطأ أثناء تشغيل قناة {channel_name}.")
    else:
        await callback_query.message.reply_text(f"الرابط لقناة {channel_name} غير متاح.")

# Stream function (your provided streaming logic)
async def stream(client, message: Message, url: str):
    from YukkiMusic.utils.logger import play_logs
    from YukkiMusic.utils.stream.stream import stream
    
    try:
        await stream(
            _,
            message,
            message.from_user.id,
            url,
            message.chat.id,
            message.from_user.first_name,
            message.chat.id,
            video=True,
            streamtype="index",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        await message.edit_text(err)
    await play_logs(message, streamtype="• ارسل الرابط صحيح .")
