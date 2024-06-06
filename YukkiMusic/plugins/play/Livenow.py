from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.errors import ChatAdminRequired
from YukkiMusic import app
from strings.filters import command
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import config

# Channels and their corresponding stream URLs
channel_streams = {
    "Channel 1": "http://ns8.indexforce.com:1935/home/mystream/chunklist_w921666703.m3u8",
    "Channel 2": "http://example.com/stream2.m3u8",
    "Channel 3": "http://example.com/stream3.m3u8",
}

# Function to create inline keyboard with channel buttons
def create_channel_buttons():
    buttons = []
    for channel_name, stream_url in channel_streams.items():
        buttons.append([InlineKeyboardButton(channel_name, callback_data=f"play_{stream_url}")])
    return InlineKeyboardMarkup(buttons)


# Function to handle callback from channel buttons
@Client.on_callback_query(filters.regex(r"^play_"))
async def callback_play_button(client, callback_query):
    mystic = await callback_query.message.edit_text("Starting the channel...")
    stream_url = callback_query.data.split("_", 1)[1]
    group_call = GroupCall(client, GroupCall.MTPROTO_CLIENT_TYPE.PYROGRAM)
    
    try:
        await group_call.start(callback_query.message.chat.id)
    except GroupCallNotFound:
        await mystic.edit_text("You must be in an active group call to play the live stream.")
        return
    
    try:
        await group_call.join(callback_query.message.chat.id)
        await group_call.start_audio(stream_url)
    except Exception as e:
        await mystic.edit_text(f"An error occurred while starting the live stream: {e}")
        await group_call.stop()
        return
    
    await mystic.edit_text(f"Started playing channel: {stream_url}")


# Function to handle commands and send inline keyboard
@Client.on_message(command(["channels"]))
async def send_channels(client, message):
    buttons = create_channel_buttons()
    await message.reply_text("Select a channel to play:", reply_markup=buttons)
