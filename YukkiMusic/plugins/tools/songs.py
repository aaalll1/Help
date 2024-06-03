from YukkiMusic import app
import os
import re
import requests
import yt_dlp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from config import SUPPORT_CHANNEL

def is_valid_youtube_url(url):
    # Check if the provided URL is a valid YouTube URL
    return url.startswith(("https://www.youtube.com", "http://www.youtube.com", "youtube.com"))

def extract_video_id(url):
    # Extract video ID from YouTube URL
    video_id = None
    if is_valid_youtube_url(url):
        if "v=" in url:
            video_id = url.split("v=")[1]
            if '&' in video_id:
                video_id = video_id.split('&')[0]
        elif "youtu.be" in url:
            video_id = url.split("/")[-1]
        else:
            video_id = None
    return video_id

@app.on_message(filters.command(["يوت", "yt", "تنزيل", "بحث"]))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    m = await message.reply_text("- جارِ البحث ...", quote=True)

    query = " ".join(str(i) for i in message.command[1:])
    ydl_opts_audio = {
        "format": "bestaudio[ext=m4a]",
    }
    ydl_opts_video = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
    }

    try:
        if is_valid_youtube_url(query):
            # If it's a valid YouTube URL, use it directly
            link = query
            video_id = extract_video_id(link)
            if video_id:
                results = [{
                    'title': '',
                    'url_suffix': f'/watch?v={video_id}',
                    'thumbnails': [''],
                    'duration': ''
                }]
            else:
                raise Exception("Invalid YouTube URL.")
        else:
            # Perform a search using the provided keyword
            results = YoutubeSearch(query, max_results=5).to_dict()
            if not results:
                raise Exception("لم يتم العثور على نتائج.")

            link = f"https://youtube.com{results[0]['url_suffix']}"

            # Check if it's a video URL or audio URL
            if not results[0].get("duration"):
                ydl_opts = ydl_opts_audio
            else:
                ydl_opts = ydl_opts_video

        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        # Replace invalid characters in the filename
        thumb_name = thumb_name.replace("/", "")
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

        await m.edit_text("- جارِ التحميل، يرجى الانتظار قليلاً ...")
        file_name = ''
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=False)
                file_name = ydl.prepare_filename(info_dict)
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

            if not results[0].get("duration"):
                # If it's an audio URL, reply as audio
                await message.reply_audio(
                    audio=file_name,
                    caption=rep,
                    thumb=thumb_name,
                    title=title,
                    duration=dur,
                    reply_markup=visit_butt,
                )
            else:
                # If it's a video URL, reply as video
                await message.reply_video(
                    file_name,
                    duration=int(info_dict["duration"]),
                    thumb=thumb_name,
                    caption=rep,
                    reply_markup=visit_butt,
                )

            await m.delete()

        except Exception as ex:
            error_message = f"- فشل في التحميل من YouTube.\n\n**السبب :** `{ex}`"
            await m.edit_text(error_message)

        # Remove temporary files after upload
        try:
            if file_name:
                os.remove(file_name)
            os.remove(thumb_name)
        except Exception as ex:
            error_message = f"- فشل في حذف الملفات المؤقتة.\n\n**السبب :** `{ex}`"
            await m.edit_text(error_message)

    except Exception as ex:
        error_message = f"- فشل البحث.\n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

@app.on_message(filters.text & ~filters.command(["يوت", "yt", "تنزيل", "بحث"]))
async def handle_text_message(client, message):
    text = message.text.strip()
    if text.startswith("يوت "):
        query = text[4:].strip()
        m = await message.reply_text("- جارِ البحث ...", quote=True)

        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
        }

        try:
            # Perform a search using the provided keyword
            results = YoutubeSearch(query, max_results=5).to_dict()
            if not results:
                raise Exception("لم يتم العثور على نتائج.")

            link = f"https://youtube.com{results[0]['url_suffix']}"

            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            # Replace invalid characters in the filename
            thumb_name = thumb_name.replace("/", "")
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=False)
                file_name = ydl.prepare_filename(info_dict)
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

            # Reply as audio
            await message.reply_audio(
                audio=file_name,
                caption=rep,
                thumb=thumb_name,
                title=title,
                duration=dur,
                reply_markup=visit_butt,
            )

            await m.delete()

        except Exception as ex:
            error_message = f"- فشل البحث.\n\n**السبب :** `{ex}`"
            await m.edit_text(error_message)

        # Remove temporary files after upload
        try:
            os.remove(file_name)
            os.remove(thumb_name)
        except Exception as ex:
            error_message = f"- فشل في حذف الملفات المؤقتة.\n\n**السبب :** `{ex}`"
            await m.edit_text(error_message)

    else:
        return

@app.on_message(filters.command(["معقول", "search"]))
async def download_video(_, message: Message):
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
    }

    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        # Replace invalid characters in the filename
        title = re.sub(r'[\\/*?:"<>|]', '', title)
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        with open(thumb_name, "wb") as file:
            file.write(thumb.content)
    except Exception as e:
        return await message.reply(f"🚫 **خطأ:** {e}")

    try:
        msg = await message.reply("- جارِ البحث ...")
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **خطأ:** {e}")

    thumb_path = f"thumb{title}.jpg"
    if not os.path.exists(thumb_path):
        return await msg.edit(f"🚫 **خطأ:** لم يتم العثور على ملف الصورة!")

    await msg.edit("- جارِ تحميل الفيديو، يرجى الانتظار قليلاً ...")
    await message.reply_video(
        file_name,
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
