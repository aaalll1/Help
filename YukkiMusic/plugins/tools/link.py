from YukkiMusic import app
import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import yt_dlp
from config import SUPPORT_CHANNEL
from youtube_search import YoutubeSearch

# Function to check if the provided URL is a valid YouTube URL
def is_valid_youtube_url(url):
    return url.startswith(("https://www.youtube.com", "http://www.youtube.com", "youtube.com"))

# Command handler for '/رابط'
@app.on_message(filters.command(["رابط"]))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    
    m = await message.reply_text("⦗ جارِ البحث يرجى الانتضار ⦘", quote=True)

    query = " ".join(str(i) for i in message.command[1:])
    ydl_opts = {"format": "bestaudio[ext=m4a]"}

    try:
        if is_valid_youtube_url(query):
            # If it's a valid YouTube URL, use it directly
            link = query
        else:
            # Otherwise, perform a search using the provided keyword
            results = YoutubeSearch(query, max_results=1).to_dict()
            if not results:
                raise Exception("- لايوجد نتائج بحث.")

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
        error_message = f"- فشل في البحث عن الفيديو. \n\n**السبب :** `{ex}`"
        return await m.edit_text(error_message)

    await m.edit_text("⦗ جارِ التحميل، يرجى الانتظار قليلاً ... ⦘")
    audio_file = ''
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        rep = f"**• by :** {message.from_user.first_name}"

        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60

        visit_butt = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⦗ Источник ⦘", url=SUPPORT_CHANNEL)],
            ]
        )
        # Reply to the user who initiated the search
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

    # Remove temporary files after audio upload
    try:
        if audio_file:
            os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as ex:
        error_message = f"- فشل في حذف الملفات المؤقتة. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)
