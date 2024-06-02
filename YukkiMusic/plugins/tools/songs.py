import os
import re
import requests
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.raw.functions.messages import GetWebPagePreview
from youtube_search import YoutubeSearch
from YukkiMusic import app

def is_valid_youtube_url(url):
    # Check if the provided URL is a valid YouTube URL
    return re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', url)

@app.on_message(filters.command(["يوت", "yt", "تنزيل", "بحث"]))
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
            # Using pyrogram to get results for channels, groups and bot's private chats.
            preview = await app.send(GetWebPagePreview(query))
            if not preview:
                raise Exception("- لايوجد بحث .")
            
            link = preview
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

        title = info_dict.get('title', 'Unknown')
        duration = info_dict.get('duration')

        rep = f"**- الأسم :** [{title[:23]}]({link})\n**- الوقت :** `{duration}`\n**- بواسطة  :** {message.from_user.first_name}"

        secmul, dur, dur_arr = 1, 0, str(duration).split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60

        share_button = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="مشاركة الصوت", switch_inline_query=audio_file)],
            ]
        )

        # Reply to the user who initiated the search
        await app.send_message(
            chat_id=message.chat.id,
            text=rep,
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
    except Exception as ex:
        error_message = f"- فشل في حذف الملفات المؤقتة. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

@app.on_message(filters.command(["تحميل", "video"]))
async def video_search(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        # إزالة الأحرف غير الصحيحة من اسم الملف
        title = re.sub(r'[\\/*?:"<>|]', '', title)
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        with open(thumb_name, "wb") as file:
            file.write(thumb.content)
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("- يتم البحث الان .")
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **error:** {e}")
    thumb_path = f"thumb{title}.jpg"
    if not os.path.exists(thumb_path):
        return await msg.edit(f"🚫 **error:** Thumb file not found!")
    
    await msg.edit("- تم الرفع انتضر قليلاً .")
    await app.send_video(
        chat_id=message.chat.id,
        video=file_name,
        duration=int(ytdl_data["duration"]),
        thumb=thumb_path,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        os.remove(thumb_path)
        await msg.delete()
    except Exception as ex:
        print(f"- فشل : {ex}")
