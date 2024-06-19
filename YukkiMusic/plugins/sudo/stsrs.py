import json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# تعريف ملف التخزين
storage_file = "user_storage.json"

# تحميل المستخدمين المخزنين إذا كانوا موجودين
try:
    with open(storage_file, "r") as file:
        stored_data = json.load(file)
except FileNotFoundError:
    stored_data = {
        'active_users': [],
        'banned_from_bot': []  # قائمة المستخدمين الذين حظروا البوت
    }

# تعريف الأمر /start
@app.on_message(filters.command("start"))
def start_command(client, message):
    user_id = message.from_user.id
    if user_id not in stored_data['active_users'] and user_id not in stored_data['banned_from_bot']:
        stored_data['active_users'].append(user_id)
        save_data()

# تعريف الأمر /ban
@app.on_message(filters.command("ban"))
def ban_command(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        if user_id not in stored_data['banned_from_bot']:
            stored_data['banned_from_bot'].append(user_id)
            if user_id in stored_data['active_users']:
                stored_data['active_users'].remove(user_id)
            save_data()
            message.reply_text(f"تم حظر المستخدم {user_id} من استخدام البوت")

# تعريف الأمر /unban
@app.on_message(filters.command("unban"))
def unban_command(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        if user_id in stored_data['banned_from_bot']:
            stored_data['banned_from_bot'].remove(user_id)
            save_data()
            message.reply_text(f"تم إلغاء حظر المستخدم {user_id} من استخدام البوت")

# تعريف الأمر /banlist
@app.on_message(filters.command("banlist"))
def banlist_command(client, message):
    banned_users = "\n".join([str(user_id) for user_id in stored_data['banned_from_bot']])
    message.reply_text(f"قائمة المستخدمين المحظورين من استخدام البوت:\n{banned_users}")

# تعريف الأمر /stats
@app.on_message(filters.command("stats"))
def stats_command(client, message):
    # إعداد أزرار الإحصائيات باستخدام InlineKeyboardMarkup
    keyboard = [
        [
            InlineKeyboardButton("المستخدمين النشطين", callback_data='stats_active'),
            InlineKeyboardButton(f"المستخدمين المحظورين ({len(stored_data['banned_from_bot'])})", callback_data='stats_banned_from_bot')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # إرسال الأزرار كرد على الرسالة الأصلية
    message.reply_text("إحصائيات البوت:", reply_markup=reply_markup)

# تعريف التفاعل مع الأزرار
@app.on_callback_query()
def button(client, callback_query):
    if callback_query.data == 'stats_active':
        callback_query.answer(f"المستخدمين النشطين: {len(stored_data['active_users'])}")
    elif callback_query.data == 'stats_banned_from_bot':
        callback_query.answer(f"المستخدمين المحظورين: {len(stored_data['banned_from_bot'])}")

# دالة لحفظ البيانات في ملف نصي
def save_data():
    with open(storage_file, "w") as file:
        json.dump(stored_data, file)
