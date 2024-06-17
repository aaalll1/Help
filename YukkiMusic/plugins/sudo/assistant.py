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

async def eor(message: Message, text: str):
    await message.reply_text(text)

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

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.strftime("%Y-%m-%d")

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
                period_name += ""
            result.append(f"{period_value} {period_name}")

    return "و".join(result[:3])

# بنك البوت
@app.on_message(command("بنك"))
async def ping_pong(c: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("-› انتضر قليلاً .")
    delta_ping = time() - start
    await m_reply.edit_text(f"-› بنك البوت : {delta_ping * 1000:.3f} ثانية")

# مدة التشغيل
@app.on_message(command(["مدة التشغيل", "مده التشغيل", "ساعات التشغيل"]))
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"-› هذا هو عدد ساعات تشغيل البوت\n⎯ ⎯ ⎯ ⎯\n-› تم تشغيل البوت منذً: {uptime}\n-› تاريخ بدء التشغيل: {START_TIME_ISO}"
    )
