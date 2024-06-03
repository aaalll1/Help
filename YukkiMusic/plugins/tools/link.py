import os
import requests
import yt_dlp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from YukkiMusic import app
from config import SUPPORT_CHANNEL

def is_valid_youtube_url(url):
    # Check if the provided URL is a valid YouTube URL
    return url.startswith(("https://www.youtube.com", "http://www.youtube.com", "youtube.com"))


@app.on_message(filters.command(["رابط"]))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass

    m = await message.reply_text("⦗ جارِ البحث يرجى الانتضار ⦘", quote=True)

    query = " ".join(str(i) for i in message.command[1:])

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "default_search": "auto",
            "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=False)
            if 'entries' in info_dict:
                info_dict = info_dict['entries'][0]
            link = info_dict['formats'][0]['url']
            title = info_dict['title']
            thumbnail = info_dict['thumbnail']
            duration = info_dict['duration']

        thumb_name = f"{title}.jpg"
        thumb_name = thumb_name.replace("/", "")
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

    except Exception as ex:
        error_message = f"- فشل .\n\n**السبب :** `{ex}`"
        return await m.edit_text(error_message)

    await m.edit_text("⦗ جارِ التحميل، يرجى الانتظار قليلاً ... ⦘")

    audio_file = f"{title}.m4a"
    try:
        await app.send_chat_action(message.chat.id, "record_audio")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])

        rep = f"**• by :** {message.from_user.first_name}"

        secmul, dur = 1, duration
        for i in range(len(dur.split(":")) - 1, -1, -1):
            dur += int(dur[i]) * secmul
            secmul *= 60

        visit_butt = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⦗ Источник ⦘", url=SUPPORT_CHANNEL)],
            ]
        )

        await message.reply_audio(
            audio=audio_file,
            caption=rep,
            thumb=thumb_name,
            title=title,
            duration=dur,
            reply_markup=visit_butt,
        )

        await m.delete()

    except Exception as ex:
        error_message = f"- فشل في تحميل الفيديو من YouTube. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

    try:
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if os.path.exists(thumb_name):
            os.remove(thumb_name)
    except Exception as ex:
        error_message = f"- فشل في حذف الملفات المؤقتة. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)
