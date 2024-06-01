from YukkiMusic import app
from strings.filters import command
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, Message
from config import OWNER
from YukkiMusic.misc import SUDOERS

# تحديد لوحة المفاتيح
keyboard_main = ReplyKeyboardMarkup(
    [
        [('⦗ فتح الكيبورد ⦘')],
        [('⦗ اعادة تشغيل ⦘'), ('⦗ تحديث السورس ⦘')],
        [('حذف الاعضاء الفيك'), ('حذف الجروبات الفيك')],
        [('الاصدار'), ('تحديث السورس'), ('سرعه السيرفر')],
        [('اذاعه للمستخدمين'), ('اذاعه للجروبات')],
        [('اذاعه للمطورين'), ('اذاعه للاساسيين'), ('اذاعه قنوات')],
        [('اذاعه للكل'), ('توجيه للكل')],
        [('توجيه للمستخدمين'), ('توجيه للجروبات'), ('توجيه للقنوات')],
        [('توجيه للاساسيين'), ('توجيه للمطورين')],
        [('⦗ حذف الكيبورد ⦘')]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

keyboard_remove = ReplyKeyboardMarkup(
    [
        [('⦗ اغلاق الكيبورد ⦘')],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# أمر لإضافة مطور سودو جديد
@app.on_message(command("اضف سودو") & filters.user(OWNER))
async def add_sudo_command(client, message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        SUDOERS.add(user_id)
        await message.reply_text(f'تمت إضافة المستخدم بمعرف {user_id} كمطور سودو.')
    else:
        await message.reply_text('الرجاء الرد على رسالة المستخدم الذي تريد إضافته كمطور سودو.')

# استيراد SUDOERS
from YukkiMusic.misc import SUDOERS
