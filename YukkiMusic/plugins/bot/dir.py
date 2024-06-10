

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from strings.filters import command
from YukkiMusic import app

pending_broadcasts = {}

@app.on_message(command(["broadcast"]))
async def initiate_broadcast(c: Client, message: Message):
    await message.reply_text("📣 ارسل الاذاعة الآن.")
    pending_broadcasts[message.from_user.id] = "broadcast"

@app.on_message(command(["broadcast_pin"]))
async def initiate_broadcast_pin(c: Client, message: Message):
    await message.reply_text("📣 ارسل الاذاعة الآن ليتم تثبيتها.")
    pending_broadcasts[message.from_user.id] = "broadcast_pin"

@app.on_message(filters.reply & filters.user(pending_broadcasts.keys()))
async def handle_broadcast(c: Client, message: Message):
    if message.from_user.id not in pending_broadcasts:
        return

    command = pending_broadcasts.pop(message.from_user.id)
    if command == "broadcast":
        await broadcast_message(c, message, pin=False)
    elif command == "broadcast_pin":
        await broadcast_message(c, message, pin=True)

async def broadcast_message(c: Client, message: Message, pin: bool):
    if not message.reply_to_message:
        await message.reply_text("🚫 لم يتم الرد على رسالة.")
        return

    x = message.reply_to_message.message_id
    y = message.chat.id
    sent = 0
    pinned = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.forward_messages(i, y, x)
            if pin:
                try:
                    await m.pin(disable_notification=True)
                    pinned += 1
                except Exception:
                    pass
            await c.send_message(i, "✅ تم نشر الإذاعة في هذه المجموعة.")
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    if pin:
        await message.reply_text(
            f"✅ اكتمل البث في {sent} مجموعة.\n📌 مع {pinned} تثبيت في المجموعة."
        )
    else:
        await message.reply_text(f"✅ اكتمل البث في {sent} مجموعة.")

@app.on_message(command(["الاحصائيات"]))
async def bot_statistic(c: Client, message: Message):
    name = me_bot.first_name
    chat_id = message.chat.id
    msg = await c.send_message(
        chat_id, "❖ جاري جمع الاحصائيات..."
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
📊 الاحصائيات الحالية لـ -› :`

-›  **عدد المجموعات** : `{served_chats}`
-›  **عدد المستخدمين** : `{served_users}`
-›  **عدد المحظورين** : `{gbans_usertl}`
"""
    await msg.edit(tgm, disable_web_page_preview=True)
