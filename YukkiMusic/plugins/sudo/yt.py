from pyrogram import Client, filters
from pyrogram.types import Message
from YukkiMusic import app

# تعريف الأمر /broadcast ودالته
@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast(client, message):
    await message.reply("أرسل الإذاعة الآن.")

    response = await app.listen(filters.private & ~filters.me & ~filters.command)
    broadcast_text = response.text

    # الحصول على قائمة المجموعات التي يمكن إرسال الإذاعة لها
    async for dialog in app.iter_dialogs():
        if dialog.chat.type in {"group", "supergroup"}:
            try:
                await app.send_message(dialog.chat.id, broadcast_text)
            except Exception as e:
                print(f"Failed to send broadcast to {dialog.chat.id}: {str(e)}")

    # إرسال رسالة تأكيد بنجاح الإذاعة وعدد المجموعات التي تم إرسال الإذاعة لها
    await message.reply(f"تم بنجاح إرسال الإذاعة إلى {len(app.iter_dialogs())} مجموعة.") 
