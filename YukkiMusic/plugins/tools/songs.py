from YukkiMusic import app
import os
import re
import requests
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from config import SUPPORT_CHANNEL

def extract_video_id(url):
    # Extract video ID from various YouTube URL formats
    # https://stackoverflow.com/a/7936523
    query = url.split("?")[-1]
    return re.search("(?<=v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v=|youtube.com\/watch\?v=|youtu.be\/)[^#\&\?]*", query).group(0)

def is_valid_youtube_url(url):
    # Check if the provided URL is a valid YouTube URL
    return any(url.startswith(prefix) for prefix in ["https://www.youtube.com", "http://www.youtube.com", "youtube.com", "https://youtu.be", "http://youtu.be", "youtu.be"])

# Command handler for /yt, /يوت, /تنزيل, /بحث
@app.on_message(filters.command(["يوت", "yt", "تنزيل", "بحث"]) & (filters.private | filters.group))
async def song(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    m = await message.reply_text("- يتم البحث الان .", quote=True)

    query = " ".join(str(i) for i in message.command[1:])
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
    }

    try:
        if is_valid_youtube_url(query):
            # If it's a valid YouTube URL, use it directly
            video_id = extract_video_id(query)
            link = f"https://youtube.com/watch?v={video_id}"
        else:
            # Perform a search using the provided keyword
            results = YoutubeSearch(query, max_results=5).to_dict()
            if not results:
                raise Exception("- لايوجد بحث .")
            
            link = f"https://youtube.com{results[0]['url_suffix']}"

        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        # Replace invalid characters in the filename
        thumb_name = thumb_name.replace("/", "")
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as ex:
        error_message = f"- فشل .\n\n**السبب :** `{ex}`"
        return await m.edit_text(error_message)

    await m.edit_text("- تم الرفع انتضر قليلاً .")
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

        visit_butt = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="- المنشئ .", url=SUPPORT_CHANNEL)],
            ]
        )

        # Reply to the user who initiated the search
        if message.chat.type == "private":
            await message.reply_audio(
                audio=audio_file,
                caption=rep,
                thumb=thumb_name,
                title=title,
                duration=dur,
                reply_markup=visit_butt,
            )
        else:
            await m.reply_audio(
                audio=audio_file,
                caption=rep,
                thumb=thumb_name,
                title=title,
                duration=dur,
                reply_markup=visit_butt,
                quote=True,
            )

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
