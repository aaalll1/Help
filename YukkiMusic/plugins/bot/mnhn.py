from YukkiMusic import app 
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

# قائمة تخزين المجموعات التي يتم فيها الإشارة
spam_chats = []

@app.on_message(filters.command(["منشن"]) & filters.reply)
async def mention_reply(client, message):
    chat_id = message.chat.id
    
    if message.chat.type == "private":
        return await message.reply("هذا الأمر متاح فقط في المجموعات.")
    
    # التحقق مما إذا كان المستخدم مسؤولًا في المجموعة
    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
        is_admin = participant.status in ("administrator", "creator")
    except UserNotParticipant:
        pass
    
    # التحقق مما إذا كان المستخدم مسؤولًا
    if not is_admin:
        return await message.reply("يجب أن تكون مسؤولاً لتنفيذ هذا الأمر.")
    
    # فحص إذا كان هناك رد على الرسالة والتحقق من وجود نص فيها
    reply_message = message.reply_to_message
    if reply_message.from_user:
        user = reply_message.from_user
        user_mention = f"[{user.first_name}](tg://user?id={user.id})"
        mention_text = f"{user_mention} {reply_message.text}" if reply_message.text else user_mention
    else:
        user_id = reply_message.from_user.id
        user_mention = f"[{user_id}](tg://user?id={user_id})"
        mention_text = f"{user_mention} {reply_message.text}" if reply_message.text else user_mention
    
    # إرسال الإشارة وحذف الرسالة الأصلية
    await message.reply(mention_text, disable_web_page_preview=True)
    await message.delete()

# أمر لإيقاف عملية الإشار
@app.on_message(filters.command(["وقف", "قف"]))
async def cancel_spam(client, message):
    # التحقق مما إذا كانت المجموعة موجودة في قائمة الإشارة
    if not message.chat.id in spam_chats:
        return await message.reply("لا يوجد عمليات إشارة جارية حاليًا.")
    
    # التحقق مما إذا كان المستخدم مسؤولًا في المجموعة
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
        is_admin = participant.status in ("administrator", "creator")
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
