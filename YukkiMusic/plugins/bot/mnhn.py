from YukkiMusic import app 
import asyncio
import random
from strings.filters import command
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

@app.on_message(command(["منشن","@all","نادي الكل"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("-› هذا الأمر فقط في المجموعات .")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("-› هذا الأمر فقط للمشرفين .")

    if message.reply_to_message and message.text:
        return await message.reply("-› اكتب منشن والرسالة التي تريد منشها \n-› مثلاً منشن صباح الخير .\n-› ولأيقاف المنشن اكتب ستوب .")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("-› اكتب منشن والرسالة التي تريد منشها \n-› مثلاً منشن صباح الخير .\n-› ولأيقاف المنشن اكتب ستوب .")
    else:
        return await message.reply("-› اكتب منشن والرسالة التي تريد منشها \n-› مثلاً منشن صباح الخير .\n-› ولأيقاف المنشن اكتب ستوب .")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{random.choice(usrtxt)}\n\n"
                await client.send_message(chat_id, txt)
                await asyncio.sleep(1)
                usrnum = 0
                usrtxt = ""
            elif mode == "text_on_reply":
                await msg.reply(f"{usrtxt}")
                await asyncio.sleep(1)
                usrnum = 0
                usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(command(["منشن ايقاف", "ستوب"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("-› هذا الأمر فقط في المجموعات.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("-› هذا الأمر فقط للمشرفين .")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("-› تم الايقاف .")
