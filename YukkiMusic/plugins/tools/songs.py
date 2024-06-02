import os
import re
import requests
import yt_dlp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from AarohiX import app
from config import SUPPORT_CHAT

# دالة لفحص ما إذا كانت الرسالة تأتي من الخاص أو من قناة أو مجموعة
def is_private_or_group_or_channel(message: Message):
    return message.chat.type in {"private", "group", "supergroup", "channel"}

# دالة لفحص ما إذا كانت الرابط صالحة ليوتيوب
def is_valid_youtube_url(url):
    return url.startswith(("https://www.youtube.com", "http://www.youtube.com", "youtube.com"))

@app.on_message(filters.command(["يوت", "yt", "تنزيل", "بحث"]) & filters.create(is_private_or_group_or_channel))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    m = await message.reply_text("- يتم البحث الان .", quote=True)

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

        share_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="مشاركة الصوت", switch_inline_query=audio_file)],
            ]
        )

        # Reply to the user who initiated the search
        await message.reply_audio(
            audio=audio_file,
            caption=rep,
            thumb=thumb_name,
            title=title,
            duration=dur,
            reply_markup=share_button,
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
