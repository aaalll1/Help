import os
import re
import requests
import yt_dlp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from YukkiMusic import app
from config import SUPPORT_CHANNEL, Muntazer

ydl_opts = {
    "format": "best",
    "keepvideo": True,
    "prefer_ffmpeg": False,
    "geo_bypass": True,
    "outtmpl": "%(title)s.%(ext)s",
    "quite": True,
}

@app.on_message(filters.command(["يوت", "yt", "تنزيل", "بحث"]))
async def song(client, message):
    try:
        await message.delete()
    except:
        pass
    
    # تحقق من الاشتراك الإجباري
    await must_join_channel(app, message)

    m = await message.reply_text("⦗ جارِ البحث يرجى الانتضار ⦘", quote=True)

    query = " ".join(message.command[1:])

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
        duration = results[0]["duration"]

        msg = await message.reply("⦗ جارِ التحميل، يرجى الانتظار قليلاً ... ⦘")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
                ytdl_data = ytdl.extract_info(link, download=True)
                file_name = ytdl.prepare_filename(ytdl_data)
        except Exception as e:
            return await msg.edit(f"🚫 **error:** {e}")
        
        await msg.edit("⦗ تم التحميل بنجاح ⦘")

        # إرسال الفيديو إلى الدردشة
        await message.reply_video(
            file_name,
            duration=int(ytdl_data["duration"]),
            caption=ytdl_data["title"],
        )

        try:
            os.remove(file_name)
        except Exception as ex:
            print(f"- فشل : {ex}")

    except Exception as ex:
        error_message = f"- فشل في تحميل الفيديو. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

@app.on_message(filters.command(["تحميل", "video"]))
async def video_search(client, message):
    query = " ".join(message.command[1:])
    try:
        # تحقق من الاشتراك الإجباري
        await must_join_channel(app, message)
  
        if is_valid_youtube_url(query):
            # If it's a valid YouTube URL, use it directly
            link = query
        else:
            return await message.reply("⦗ يرجى إدخال رابط يوتيوب صالح ⦘")

        msg = await message.reply("⦗ جارِ التحميل، يرجى الانتظار قليلاً ... ⦘")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
                ytdl_data = ytdl.extract_info(link, download=True)
                file_name = ytdl.prepare_filename(ytdl_data)
        except Exception as e:
            return await msg.edit(f"🚫 **error:** {e}")

        await msg.edit("⦗ تم التحميل بنجاح ⦘")

        # إرسال الفيديو إلى الدردشة
        await message.reply_video(
            file_name,
            duration=int(ytdl_data["duration"]),
            caption=ytdl_data["title"],
        )

        try:
            os.remove(file_name)
        except Exception as ex:
            print(f"- فشل : {ex}")

    except Exception as e:
        return await msg.edit(f"🚫 **error:** {e}")

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
        print(f"I'm not admin in the MUST_JOIN chat {Muntazer}!")
