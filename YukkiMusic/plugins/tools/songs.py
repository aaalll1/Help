import os
import re
import requests
import yt_dlp
from strings.filters import command
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from YukkiMusic import app
from config import SUPPORT_CHANNEL, Muntazer
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatWriteForbidden


# دالة للتحقق من اشتراك المستخدم في القناة
async def must_join_channel(app, msg):
    if not Muntazer:
        return
    try:
        if msg.from_user is None:
            return
        
        try:
            await app.get_chat_member(Muntazer, msg.from_user.id)
        except UserNotParticipant:
            if Muntazer.isalpha():
                link = "https://t.me/" + Muntazer
            else:
                chat_info = await app.get_chat(Muntazer)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    f"~︙عليك الأشتراك في قناة البوت \n~︙قناة البوت : @{Muntazer}.",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⦗ قناة البوت ⦘", url=link)]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I m not admin in the MUST_JOIN chat {Muntazer}!")


def is_valid_youtube_url(url):
    # Check if the provided URL is a valid YouTube URL
    return url.startswith(("https://www.youtube.com", "http://www.youtube.com", "youtube.com"))


@app.on_message(command(["يوت", "yt", "تنزيل", "بحث"]))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    
    # تحقق من الاشتراك الإجباري
    await must_join_channel(app, message)

    m = await message.reply_text("⦗ جارِ البحث يرجى الانتضار ⦘", quote=True)

    query = " ".join(str(i) for i in message.command[1:])
    ydl_opts = {"format": "bestaudio[ext=m4a]"}

    try:
        if is_valid_youtube_url(query):
            # If it's a valid YouTube URL, use it directly
            link = query
        else:
            # Otherwise, perform a search using the provided keyword
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



async def video_to_audio(link):
    try:
        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "default_search": "auto",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            if 'entries' in info_dict:
                video_url = info_dict['entries'][0]['webpage_url']
            else:
                video_url = info_dict.get('webpage_url', None)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        return audio_file, info_dict["title"], info_dict["duration"]

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

# دالة للتحميل وإرسال الملف الصوتي أو الفيديو
@app.on_message(filters.command(["رابط", "يوتيوب"]) & filters.regex(r'https?://(?:www\.)?youtube\.com\S+'))
async def youtube_audio(client, message: Message):
    try:
        await message.delete()
    except:
        pass

    # تحقق من الاشتراك الإجباري
    await must_join_channel(client, message)

    m = await message.reply_text("⦗ جارِ التحميل، يرجى الانتظار قليلاً ... ⦘", quote=True)

    try:
        link = message.text.strip()

        if "watch?v=" in link:
            # إذا كان الرابط فيديو، قم بتحويله إلى صوت
            audio_file, title, duration = await video_to_audio(link)
            if not audio_file:
                raise Exception("فشل في تحويل الفيديو إلى صوت")

        else:
            # إذا كان الرابط بالفعل صوتي، استخدمه مباشرة
            audio_file = link
            with yt_dlp.YoutubeDL({}) as ydl:
                info_dict = ydl.extract_info(link, download=False)
                title = info_dict.get("title", "ملف صوتي")
                duration = info_dict.get("duration", 0)

        rep = f"**• by :** {message.from_user.first_name}"

        visit_butt = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⦗ Источник ⦘", url=SUPPORT_CHANNEL)],
            ]
        )

        # الرد على المستخدم الذي بدأ البحث
        if audio_file.endswith(".m4a"):
            await message.reply_audio(
                audio=audio_file,
                caption=rep,
                title=title,
                duration=duration,
                reply_markup=visit_butt,
            )
        else:
            await message.reply_video(
                video=audio_file,
                caption=rep,
                title=title,
                duration=duration,
                reply_markup=visit_butt,
            )

        await m.delete()

    except Exception as ex:
        error_message = f"- فشل في تحميل الفيديو أو تحويله إلى صوت. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

    # حذف الملفات المؤقتة بعد تحميل الصوت
    try:
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)
    except Exception as ex:
        error_message = f"- فشل في حذف الملفات المؤقتة. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)


@app.on_message(command(["تحميل", "video"]))
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
        # تحقق من الاشتراك الإجباري
        await must_join_channel(app, message)
  
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
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("⦗ جارِ البحث يرجى الانتضار ⦘")
        with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **error:** {e}")
    
    thumb_path = f"thumb{title}.jpg"
    if not os.path.exists(thumb_path):
        return await msg.edit(f"🚫 **error:** Thumb file not found!")
    
    await msg.edit("⦗ جارِ التحميل، يرجى الانتظار قليلاً ... ⦘")
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
