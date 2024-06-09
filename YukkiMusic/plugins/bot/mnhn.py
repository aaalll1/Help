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




@app.on_message(command(["المالك", "صاحب الخرابه", "المنشي", "مطور السورس"]) & filters.group)
async def gak_owne(client: Client, message: Message):
    if len(message.command) >= 2:
        return 
    else:
        chat_id = message.chat.id
        command_text = message.command[0]

        if command_text in ["ملك", "مالك", "مطور"]:
            f = "administrators"
            async for member in client.iter_chat_members(chat_id, filter=f):
                if member.status == "creator":
                    id = member.user.id
                    key = InlineKeyboardMarkup([[InlineKeyboardButton(member.user.first_name, user_id=id)]])
                    m = await client.get_chat(id)
                    if m.photo:
                        photo = await app.download_media(m.photo.big_file_id)
                        return await message.reply_photo(photo, caption=f"🧞‍♂️ ¦𝙽𝙰𝙼𝙴 :{m.first_name}\n🎯 ¦𝚄𝚂𝙴𝚁 :@{m.username}\n🎃 ¦𝙸𝙳 :`{m.id}`\n💌 ¦𝙱𝙸𝙾 :{m.bio}\n✨ ¦𝙲𝙷𝙰𝚃: {message.chat.title}\n♻️ ¦𝙸𝙳.𝙲𝙷𝙰𝚃 :`{message.chat.id}`", reply_markup=key)
                    else:
                        return await message.reply("• " + member.user.mention)
        elif command_text == "مطور السورس":
            developer_id = 1854384004  # ضع هنا معرف حسابك الشخصي
            m = await client.get_chat(developer_id)
            if m.photo:
                photo = await app.download_media(m.photo.big_file_id)
                key = InlineKeyboardMarkup([[InlineKeyboardButton(m.first_name, user_id=developer_id)]])
                return await message.reply_photo(photo, caption=f"🧞‍♂️ ¦𝙽𝙰𝙼𝙴 :{m.first_name}\n🎯 ¦𝚄𝚂𝙴𝚁 :@{m.username}\n🎃 ¦𝙸𝙳 :`{m.id}`\n💌 ¦𝙱𝙸𝙾 :{m.bio}", reply_markup=key)
            else:
                return await message.reply(f"• {m.mention}"))
                    
                    

array = []
@app.on_message(command(["@all", "تاك","تاك للكل"]) & ~filters.private)
async def nummmm(client: app, message):
  if message.chat.id in array:
     return await message.reply_text("-› المنشن قيد التشغيل .")
  chek = await client.get_chat_member(message.chat.id, message.from_user.id)
  if not chek.status in ["administrator", "creator"]:
    await message.reply("-› يجب ان تكون مشرفاً كي تستخدم الأمر .")
    return
  await message.reply_text("-› جاري بدأ المنشن ، لإيقاف الامر اكتب منشن اوكف . ")")
  i = 0
  txt = ""
  zz = message.text
  if message.photo:
          photo_id = message.photo.file_id
          photo = await client.download_media(photo_id)
          zz = message.caption
  try:
   zz = zz.replace("@all","").replace("تاك","").replace("نادي الكل","")
  except:
    pass
  array.append(message.chat.id)
  async for x in client.iter_chat_members(message.chat.id):
      if message.chat.id not in array:
        return
      if not x.user.is_deleted:
       i += 1
       txt += f" {x.user.mention} ،"
       if i == 5:
        try:
              if not message.photo:
                    await client.send_message(message.chat.id, f"{zz}\n{txt}")
              else:
                    await client.send_photo(message.chat.id, photo=photo, caption=f"{zz}\n{txt}")
              i = 0
              txt = ""
              await asyncio.sleep(2)
        except FloodWait as e:
                    flood_time = int(e.x)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
        except Exception:
              array.remove(message.chat.id)
  array.remove(message.chat.id)


@app.on_message(command(["منشن اوكف", "/cancel","منشن ايقاف"]))
async def stop(client, message):
  chek = await client.get_chat_member(message.chat.id, message.from_user.id)
  if not chek.status in ["administrator", "creator"]:
    await message.reply("-› يجب ان تكون مشرفاً كي تستخدم الأمر .")
    return
  if message.chat.id not in array:
     await message.reply("-› تم منذ قليل ايقافة .")
     return 
  if message.chat.id in array:
    array.remove(message.chat.id)
    await message.reply("-› تم ايقاف المنشن .")
    return




