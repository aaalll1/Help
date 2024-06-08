
import os
from inspect import getfullargspec
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import get_client
from strings.filters import command
# Your USER client import goes here
# from YukkiMusic.core.userbot import USER

@app.on_message(command("setpfp") & SUDOERS)
async def set_pfp(client, message):
    from YukkiMusic.core.userbot import assistants

    if (
        not message.reply_to_message
        or not message.reply_to_message.photo
        or not message.reply_to_message.video
    ):
        return await eor(message, text="Reply to a photo or video")
    for num in assistants:
        client = await get_client(num)
        photo = await message.reply_to_message.download()
        if message.reply_to_message.photo:
            try:
                await client.set_profile_photo(photo=photo)
                await eor(message, text="Successfully Changed PFP.")
                os.remove(photo)
            except Exception as e:
                await eor(message, text=str(e))
                os.remove(photo)
        if message.reply_to_message.video:
            try:
                await client.set_profile_photo(video=photo)
                await eor(message, text="Successfully Changed PFP.")
                os.remove(photo)
            except Exception as e:
                await eor(message, text=str(e))
                os.remove(photo)


@app.on_message(command("setbio") & SUDOERS)
async def set_bio(client, message):
    from YukkiMusic.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text="Give some text to set as bio.")
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await eor(message, text="Changed Bio.")
        except Exception as e:
            await eor(message, text=str(e))
    else:
        return await eor(message, text="Give some text to set as bio.")


@app.on_message(command("setname") & SUDOERS)
async def set_name(client, message):
    from YukkiMusic.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text="Give some text to set as name.")
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await eor(message, text=f"name Changed to {name} .")
        except Exception as e:
            await eor(message, text=str(e))
    else:
        return await eor(message, text="Give some text to set as name.")


@app.on_message(command("delpfp") & SUDOERS)
async def del_pfp(client, message):
    from YukkiMusic.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos(photos[0].file_id)
                await eor(message, text="Successfully deleted photo")
            else:
                await eor(message, text="No profile photos found.")
        except Exception as e:
            await eor(message, text=str(e))


@app.on_message(command("delallpfp") & SUDOERS)
async def delall_pfp(client, message):
    from YukkiMusic.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos[1:]])
                await eor(message, text="Successfully deleted photos")
            else:
                await eor(message, text="No profile photos found.")
        except Exception as e:
            await eor(message, text=str(e))


@app.on_message(command(["ضبط", "اضبط", "vol"]))
async def change_volume(c: Client, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("الاستخدام: `.اضبط` (`0-200`)")
    
    a = await c.get_chat_member(m.chat.id, me_user.id)
    if not a.can_manage_voice_chats:
        return await m.reply_text(
            "👍🏻 لاستخدام هذا الأمر، عليك رفع حساب المساعد بصلاح نية إدارة الدردشات الصوتية"
        )
    
    volume_range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await calls.change_volume_call(chat_id, volume=int(volume_range))
            await m.reply_text(f"-› **تم ضبط الصوت إلى** `{volume_range}`%")
        except Exception as e:
            await m.reply_text(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply_text("معليش، ما في شي مشتغل يا عيني 🌵")

@app.on_message(command(["بنك"]))
async def ping_pong(c: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("جاري حساب البنك...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 البنك !\n" f"⏱ `{delta_ping * 1000:.3f} مللي ثانية`")

# زمن البدء
START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.strftime("%Y-%m-%d %H:%M:%S")

# دالة لتحويل الوقت إلى صيغة قراءة الإنسان
async def _human_time_duration(seconds: int) -> str:
    periods = [
        ("سنة", 60 * 60 * 24 * 365),
        ("شهر", 60 * 60 * 24 * 30),
        ("أسبوع", 60 * 60 * 24 * 7),
        ("يوم", 60 * 60 * 24),
        ("ساعة", 60 * 60),
        ("دقيقة", 60),
        ("ثانية", 1)
    ]

    result = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value > 1:
                period_name += "s"
            result.append(f"{period_value} {period_name}")

    return ", ".join(result[:3])  # يظهر زمن عرض البرمجيات حتى ثلاث مناسبات 

@app.on_message(command(["مدة التشغيل", "مده التشغيل", "وقت التشغيل"]))
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 حالة البوت:\n"
        f"• **وقت التشغيل:** `{uptime}`\n"
        f"• **وقت البدء:** `{START_TIME_ISO}`"
    )
