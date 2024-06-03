import os
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_dl import YoutubeDL
from YukkiMusic import app
from config import SUPPORT_CHANNEL, Muntazer
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatWriteForbidden

@app.on_message(filters.command(["رابط"]))
async def song(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    
    # تحقق من الاشتراك الإجباري
    await must_join_channel(app, message)

    m = await message.reply_text("⦗ جارِ البحث يرجى الانتضار ⦘", quote=True)

    query = " ".join(str(i) for i in message.command[1:])

    try:
        if not is_valid_youtube_url(query):
            raise Exception("- الرابط غير صالح.")

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        title = info_dict.get('title', 'Unknown Title')
        duration = info_dict.get('duration', 0)

        rep = f"**• by :** {message.from_user.first_name}"
        visit_butt = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="⦗ Источник ⦘", url=SUPPORT_CHANNEL)],
            ]
        )

        await message.reply_audio(
            audio=audio_file,
            caption=rep,
            title=title,
            duration=duration,
            reply_markup=visit_butt,
        )

        await m.delete()

        # Remove temporary files after audio upload
        try:
            if audio_file:
                os.remove(audio_file)
        except Exception as ex:
            error_message = f"- فشل في حذف الملفات المؤقتة. \n\n**السبب :** `{ex}`"
            await m.edit_text(error_message)

    except Exception as ex:
        error_message = f"- فشل في تحميل الفيديو من YouTube. \n\n**السبب :** `{ex}`"
        await m.edit_text(error_message)

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
