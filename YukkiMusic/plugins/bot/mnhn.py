from YukkiMusic import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

# قائمة تخزين المجموعات التي يتم فيها الإشارة
spam_chats = []

@app.on_message(filters.command(["منشن"]))
async def mention_command(client, message):
    chat_id = message.chat.id
    
    if message.chat.type == "private":
        return await message.reply("هذا الأمر متاح فقط في المجموعات.")
    
    # التحقق مباشرة من حالة المشارك في المجموعة
    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
        is_admin = participant.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except UserNotParticipant:
        pass
    
    # التحقق مما إذا كان المستخدم مسؤولًا
    if not is_admin:
        return await message.reply("يجب أن تكون مسؤولاً لتنفيذ هذا الأمر.")
    
    # فحص إذا كان هناك رد على الرسالة والتحقق من وجود نص فيها
    if message.reply_to_message or message.text:
        # استخدام الرد إذا كان متوفرًا، وإلا فاستخدام الرسالة نفسها
        reply_message = message.reply_to_message if message.reply_to_message else message
        mention_text = reply_message.text if reply_message.text else ""
        # إرسال الإشارة لجميع أعضاء المجموعة
        async for member in await client.get_chat_members(chat_id):
            # تجاهل البوتات
            if member.user.is_bot:
                continue
            # تكوين الرابط الذي يفتح حساب المستخدم عند النقر عليه
            user_link = f"[{member.user.first_name}](tg://user?id={member.user.id})"
            # منشن لكل عضو بالرسالة مع الرابط
            await message.reply(f"{user_link} {mention_text}", disable_web_page_preview=True)
            await asyncio.sleep(4)  # تأخير لمنع الإسبام
        # حذف الرسالة الأصلية
        await message.delete()
    else:
        # استخدام الأمر بدون رد على رسالة أو إرسال رسالة مباشرة
        return await message.reply("الرجاء الرد على الرسالة التي تريد إشارتها.")

# أمر لإيقاف عملية الإشارة
@app.on_message(filters.command(["وقف", "قف"]))
async def cancel_spam(client, message):
    # التحقق مما إذا كانت المجموعة موجودة في قائمة الإشارة
    if not message.chat.id in spam_chats:
        return await message.reply("لا يوجد عمليات إشارة جارية حاليًا.")
    
    # التحقق مما إذا كان المستخدم مسؤولًا في المجموعة
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
        is_admin = participant.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except UserNotParticipant:
        pass
    
    # التحقق مما إذا كان المستخدم مسؤولًا
    if not is_admin:
        return await message.reply("يجب أن تكون مسؤولاً لإيقاف عملية الإشارة.")
    else:
        # إزالة المجموعة من قائمة الإشارة
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("تم إيقاف عملية الإشارة بنجاح.")
