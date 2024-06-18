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
@app.on_message(command("تعيين صورة النساعد","⦗ تعيين صورة المساعد ⦘") & SUDOERS)
async def set_pfp_prompt(client, message):
    user_id = message.from_user.id
    USER_STATES[user_id] = "awaiting_pfp"
    await eor(message, text="⦗ عزيزي المطور قم بالرد على هذا الرسالة وارسل الصورة الأن .⦘")

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
                if message.photo:
                    await client.set_profile_photo(photo=photo)
                await eor(message.reply_to_message, text="⦗ تم تعيين الصورة بنجاح ⦘.")
                success = True
                os.remove(photo)
                break
            except Exception as e:
                await eor(message.reply_to_message, text=str(e))
                os.remove(photo)
        
        if not success:
            await eor(message.reply_to_message, text="⦗ فشل التغيير ⦘.")
        
        USER_STATES.pop(user_id, None)

# أمر حذف صورة الملف الشخصي الحالية
@app.on_message(command("⦗ حذف صورة المساعد ⦘","حذف صورة المساعد") & SUDOERS & filters.reply)
async def del_pfp_prompt(client, message):
    user_id = message.from_user.id
    USER_STATES[user_id] = "awaiting_delpfp"
    await eor(message, text="Are you sure you want to delete the current profile picture? Reply 'yes' to confirm.")

@app.on_message(filters.text & filters.reply & SUDOERS)
async def handle_delpfp_reply(client, message):
    user_id = message.from_user.id
    if USER_STATES.get(user_id) == "awaiting_delpfp" and message.text.lower() == "yes":
        from YukkiMusic.core.userbot import assistants

        success = False
        for num in assistants:
            client = await get_client(num)
            try:
                photos = [p async for p in client.get_chat_photos("me")]
                if photos:
                    await client.delete_profile_photos(photos[0].file_id)
                    await eor(message.reply_to_message, text="⦗ تم حذف اخر صورة ⦘.")
                    success = True
                    break
                else:
                    await eor(message.reply_to_message, text="⦗ لاتوجد اي صورة في الحساب ⦘.")
            except Exception as e:
                await eor(message.reply_to_message, text=str(e))
        
        if not success:
            await eor(message.reply_to_message, text="⦗ فشل الحذف ⦘.")
        
        USER_STATES.pop(user_id, None)



@app.on_message(command("اسم المساعد") & SUDOERS)
async def set_name(client, message):
    from YukkiMusic.core.userbot import assistants

    user_id = message.from_user.id
    if len(message.command) == 1:
        await eor(message, text="⦗ قم بالرد على الاسم او اكتب الأمر مع الأسم ⦘.")
        USER_STATES[user_id] = "awaiting_name"
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        if USER_STATES.get(user_id) == "awaiting_name":
            success = False
            
            for num in assistants:
                try:
                    assistant_client = await get_client(num)
                    await assistant_client.update_profile(first_name=name)
                    await eor(message, text=f"⦗ تم تعيين الأسم {name} ⦘ .")
                    success = True
                    break
                except Exception as e:
                    await eor(message, text=f"خطأ أثناء تعيين الاسم عبر المساعد {num}: {str(e)}")

            if not success:
                await eor(message, text="فشل في تعيين الاسم.")
            
            USER_STATES.pop(user_id, None)
        else:
            await eor(message, text="لا يوجد طلب تعيين اسم متوقع حاليًا.")
    else:
        await eor(message, text="قم بإرسال النص الجديد لتعيينه كاسم.")

# أمر حذف الصورة الشخصية
@app.on_message(command("⦗ مسح صورة المساعد ⦘") & SUDOERS)
async def del_pfp(client, message):
    from YukkiMusic.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos(photos[0].file_id)
                await eor(message, text="⦗ تم حذف صورة المساعد ⦘")
            else:
                await eor(message, text="⦗ لاتوجد صور حاليا ⦘.")
        except Exception as e:
            await eor(message, text=str(e))


# أمر حذف جميع الصور الشخصية
@app.on_message(command("⦗ حذف كافة صور المساعد ⦘","حذف الصور") & SUDOERS)
async def delall_pfp(client, message):
    from YukkiMusic.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos[1:]])
                await eor(message, text="⦗ تم حذف كافة الصور ⦘")
            else:
                await eor(message, text="⦗ لاتوجد صور حالياً ⦘.")
        except Exception as e:
            await eor(message, text=str(e))

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
