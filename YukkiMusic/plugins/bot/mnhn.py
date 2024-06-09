import asyncio
import os
import time
import requests
import aiohttp
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from strings.filters import command
from YukkiMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from YukkiMusic import app
from asyncio import gather
from pyrogram.errors import FloodWait
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions



@app.on_message(command(["المالك", "صاحب الخرابه", "المنشي"]) & filters.group)
async def gak_owne(client: Client, message: Message):
      if len(message.command) >= 2:
         return 
      else:
            chat_id = message.chat.id
            f = "administrators"
            async for member in client.iter_chat_members(chat_id, filter=f):
               if member.status == "creator":
                 id = member.user.id
                 key = InlineKeyboardMarkup([[InlineKeyboardButton(member.user.first_name, user_id=id)]])
                 m = await client.get_chat(id)
                 if m.photo:
                       photo = await app.download_media(m.photo.big_file_id)
                       return await message.reply_photo(photo, caption=f"🧞‍♂️ ¦𝙽𝙰𝙼𝙴 :{m.first_name}\n🎯 ¦𝚄𝚂𝙴𝚁 :@{m.username}\n🎃 ¦𝙸𝙳 :`{m.id}`\n💌 ¦𝙱𝙸𝙾 :{m.bio}\n✨ ¦𝙲𝙷𝙰𝚃: {message.chat.title}\n♻️ ¦𝙸𝙳.𝙲𝙷𝙰𝚃 :`{message.chat.id}`",reply_markup=key)
                 else:
                    return await message.reply("• " + member.user.mention)                    

spam_chats = []

TEXT = [
    "• ادعوك الى الى الحضور هنا .",
]

@app.on_message(command(["vctag", "vctagall"], prefixes=["/", ".", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        return await message.reply("هذا الأمر مخصص للمجموعات فقط.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in ("administrator", "creator"):
            is_admin = True
    if not is_admin:
        return await message.reply("أنت لست مشرفًا، فقط المشرفين يمكنهم وضع العلامات للأعضاء.")

    if message.reply_to_message and message.text:
        return await message.reply("/Vctag ادخلوا إلى الدردشة الصوتية الآن 👈 اكتب بهذا الشكل / أو رد على أي رسالة في المرة القادمة للعلامة...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/Vctag ادخلوا إلى الدردشة الصوتية الآن 👈 اكتب بهذا الشكل / أو رد على أي رسالة في المرة القادمة للعلامة...")
    else:
        return await message.reply("/Vctag ادخلوا إلى الدردشة الصوتية الآن 👈 اكتب بهذا الشكل / أو رد على أي رسالة في المرة القادمة للعلامة...")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TEXT)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(TEXT)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(command(["cancel", "stop", "stopvctag", "vctagstop", "cancelvctag", "canceltag", "stoptag", "stoptagall", "canceltagall"]))
async def cancel_spam(client, message):
    if message.chat.id not in spam_chats:
        return await message.reply("حاليًا، لست في عملية وضع العلامات.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in ("administrator", "creator"):
            is_admin = True
    if not is_admin:
        return await message.reply("أنت لست مشرفًا، فقط المشرفين يمكنهم إيقاف عملية وضع العلامات.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("تم إلغاء عملية وضع العلامات.")
