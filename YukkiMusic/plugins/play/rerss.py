from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import OWNER


# متغير لتخزين كلمة البداية الجديدة
new_start_message = None

# يحدث عند كتابة "تغيير كلمة البداية" للمالك
@app.on_message(filters.command("تغيير كلمة البداية") & filters.user(OWNER))
async def change_start_message(_, message: Message):
    global new_start_message
    new_start_message = None  # تأكد من إعادة تعيينها
    await message.reply("أرسل كلمة البداية الجديدة لتحديثها.")

# يحدث عندما يرد المالك بكلمة البداية الجديدة
@app.on_message(filters.private & filters.user(OWNER))
async def set_new_start_message(_, message: Message):
    global new_start_message
    if new_start_message is None:
        new_start_message = message.text
        await message.reply("تم تحديث كلمة البداية بنجاح!")
