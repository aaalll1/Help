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
                if message.photo:
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

# أمر حذف صورة الملف الشخصي الحالية
@app.on_message(command("delpfp") & SUDOERS & filters.reply)
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
                    await eor(message.reply_to_message, text="Successfully deleted profile photo.")
                    success = True
                    break
                else:
                    await eor(message.reply_to_message, text="No profile photos found.")
            except Exception as e:
                await eor(message.reply_to_message, text=str(e))
        
        if not success:
            await eor(message.reply_to_message, text="Failed to delete profile photo.")
        
        USER_STATES.pop(user_id, None)


# Function to add user to contacts
async def add_to_contacts(client, user_id):
    try:
        await client.add_contact(user_id, "New Contact")  # Replace "New Contact" with the display name you want
        return True
    except Exception as e:
        print(f"Failed to add contact: {str(e)}")
        return False


# Command to add user to contacts
@app.on_message(command("اضفني") & filters.private & SUDOERS)
async def add_me_to_contacts(client, message):
    user_id = message.from_user.id
    from YukkiMusic.core.userbot import assistants  # Assuming assistants are imported correctly

    success = False
    for num in assistants:
        try:
            assistant_client = await get_client(num)
            added = await add_to_contacts(assistant_client, user_id)
            if added:
                success = True
                await eor(message, text="تمت إضافتك إلى جهات الاتصال بنجاح.")
                break
        except Exception as e:
            print(f"Error adding contact with assistant {num}: {str(e)}")

    if not success:
        await eor(message, text="فشلت عملية إضافتك إلى جهات الاتصال.")

# أمر تعيين الاسم
@app.on_message(filters.command("setname") & filters.private & SUDOERS)
async def set_name_prompt(client, message):
    user_id = message.from_user.id
    USER_STATES[user_id] = "awaiting_name"
    await eor(message, text="Please send the new name now.")

# Handling reply with the new name
@app.on_message(filters.text & filters.private & SUDOERS)
async def handle_name_reply(client, message):
    user_id = message.from_user.id
    if USER_STATES.get(user_id) == "awaiting_name":
        from YukkiMusic.core.userbot import assistants  # Assuming assistants are imported correctly

        name = message.text.strip()
        if not name:
            await eor(message, text="You didn't provide a name.")
            return

        success = False
        for num in assistants:
            try:
                client = await get_client(num)
                await client.update_profile(first_name=name)
                await eor(message, text=f"Name changed to {name} successfully.")
                success = True
                break
            except Exception as e:
                await eor(message, text=str(e))

        if not success:
            await eor(message, text="Failed to set name.")

        USER_STATES.pop(user_id, None)
# أمر حذف الصورة الشخصية
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


# أمر حذف جميع الصور الشخصية
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
