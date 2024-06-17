import os
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import get_client
from strings.filters import command

# تخزين الحالة المؤقتة لكل مستخدم
USER_STATES = {}

async def eor(message: Message, text: str):
    await message.reply_text(text)

# أمر تعيين صورة الملف الشخصي
@app.on_message(command("setpfp") & SUDOERS)
async def set_pfp_prompt(client, message):
    user_id = message.from_user.id
    USER_STATES[user_id] = "awaiting_pfp"
    await eor(message, text="Please send the new profile picture now.")

@app.on_message(filters.photo & filters.reply & SUDOERS)
async def handle_pfp_reply(client, message):
    user_id = message.from_user.id
    if USER_STATES.get(user_id) == "awaiting_pfp":
        from YukkiMusic.core.userbot import assistants

        photo = await message.download()
        success = False
        for num in assistants:
            client = await get_client(num)
            try:
                await client.set_profile_photo(photo=photo)
                await eor(message.reply_to_message, text="Successfully changed profile picture.")
                success = True
                os.remove(photo)
                break
            except Exception as e:
                await eor(message.reply_to_message, text=str(e))
                os.remove(photo)
        
        if not success:
            await eor(message.reply_to_message, text="Failed to set profile picture.")
        
        USER_STATES.pop(user_id, None)

# أمر تعيين النبذة الشخصية
@app.on_message(command("setbio") & SUDOERS)
async def set_bio_prompt(client, message):
    user_id = message.from_user.id
    USER_STATES[user_id] = "awaiting_bio"
    await eor(message, text="Please send the new bio text now.")

@app.on_message(filters.text & filters.reply & SUDOERS)
async def handle_bio_reply(client, message):
    user_id = message.from_user.id
    if USER_STATES.get(user_id) == "awaiting_bio":
        from YukkiMusic.core.userbot import assistants

        bio = message.text
        success = False
        for num in assistants:
            client = await get_client(num)
            try:
                await client.update_profile(bio=bio)
                await eor(message.reply_to_message, text="Bio changed successfully.")
                success = True
                break
            except Exception as e:
                await eor(message.reply_to_message, text=str(e))
        
        if not success:
            await eor(message.reply_to_message, text="Failed to set bio.")
        
        USER_STATES.pop(user_id, None)

# أمر تعيين الاسم
@app.on_message(command("setname") & SUDOERS)
async def set_name_prompt(client, message):
    user_id = message.from_user.id
    USER_STATES[user_id] = "awaiting_name"
    await eor(message, text="Please send the new name now.")

@app.on_message(filters.text & filters.reply & SUDOERS)
async def handle_name_reply(client, message):
    user_id = message.from_user.id
    if USER_STATES.get(user_id) == "awaiting_name":
        from YukkiMusic.core.userbot import assistants

        name = message.text
        success = False
        for num in assistants:
            client = await get_client(num)
            try:
                await client.update_profile(first_name=name)
                await eor(message.reply_to_message, text=f"Name changed to {name} successfully.")
                success = True
                break
            except Exception as e:
                await eor(message.reply_to_message, text=str(e))
        
        if not success:
            await eor(message.reply_to_message, text="Failed to set name.")
        
        USER_STATES.pop(user_id, None)

# إعداد الوقت البدء للتشغيل
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
