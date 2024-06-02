import os
import re
import requests
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from YukkiMusic import app
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatWriteForbidden
from YukkiMusic.utils.stream.stream import stream
from YukkiMusic.utils import time_to_seconds

# Function to check if the URL is a valid YouTube URL
def is_valid_youtube_url(url):
    return url.startswith(("https://www.youtube.com", "http://www.youtube.com", "youtube.com"))

# Command handler to search and send audio
@app.on_message(filters.command(["يوت", "yt", "تنزيل", "بحث"]))
async def song_group(client, message: Message):
    await song(client, message)

@app.on_message(filters.command(["يوت", "yt", "تنزيل", "بحث"]) & filters.private)
async def song_private(client, message: Message):
    await song(client, message)

async def song(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    m = await message.reply_text("- يتم البحث الآن .", quote=True)

    query = " ".join(str(i) for i in message.command[1:])
    ydl_opts = {"format": "bestaudio[ext=m4a]"}

    try:
        if is_valid_youtube_url(query):
            # If it's a valid YouTube URL, use it directly
            link = query
        else:
            # Otherwise, perform a search using the provided keyword
            with yt_dlp.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(query, download=False)
                if "_type" in info_dict and info_dict["_type"] == "playlist":
                    link = info_dict["entries"][0]["url"]
                else:
                    link = info_dict["url"]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'Unknown')
            thumbnail = info_dict.get('thumbnails', [])[0]['url']
            thumb_name = f"{title}.jpg"
            # Replace invalid characters in the filename
            thumb_name = thumb_name.replace("/", "")
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = info_dict.get('duration')

    except Exception as ex:
        error_message = f"- فشل .\n\n**السبب :** `{ex}`"
        return await m.edit_text(error_message)

    await m.edit_text("- تم الرفع انتظر قليلاً .")
    audio_file = ''
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        rep = f"**- الأسم :** [{title[:23]}]({link})\n**- الوقت :** `{duration}`\n**- بواسطة  :** {message.from_user.first_name}"

        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60

        share_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="مشاركة الصوت", switch_inline_query=audio_file)],
                [InlineKeyboardButton(text="تشغيل في المكالمة", callback_data=f"MusicStream|{audio_file}|{dur}")]
            ]
        )

        # Reply to the user who initiated the search
        await send_audio(message.chat.id, audio_file, rep, thumb_name, title, dur, share_button)

        await m.delete()

    except Exception as ex:
        error_message = f"- فشل في تحميل الفيديو من YouTube. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

    # Remove temporary files after audio upload
    try:
        if audio_file:
            os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as ex:
        error_message = f"- فشل في حذف الملفات المؤقتة. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

# Function to send audio to voice call
async def send_audio(chat_id, audio_file, caption, thumbnail, title, duration, share_button):
    try:
        await app.send_chat_action(chat_id, "upload_audio")
        with open(audio_file, "rb") as f:
            await app.send_audio(chat_id, audio=f, caption=caption, duration=duration,
                                 thumb=thumbnail, title=title, reply_markup=share_button)
    except Exception as e:
        print(f"Error in sending audio: {e}")
