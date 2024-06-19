from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from collections import defaultdict

# متغيرات لتخزين الإحصائيات
stats = defaultdict(int)  # استخدام defaultdict لتخزين العدد بشكل تلقائي

# تعريف الأمر /stats
@app.on_message(filters.command("stats"))
def stats_command(client, message):
    # إعداد أزرار الإحصائيات باستخدام InlineKeyboardMarkup
    keyboard = [
        [
            InlineKeyboardButton(f"المستخدمين النشطين: {stats['active_users']}", callback_data='stats_active'),
            InlineKeyboardButton(f"المستخدمين المحظورين: {stats['banned_users']}", callback_data='stats_banned')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # إرسال الأزرار كرد على الرسالة الأصلية
    message.reply_text("إحصائيات البوت:", reply_markup=reply_markup)

# تعريف التفاعل مع الأزرار
@app.on_callback_query()
def button(client, callback_query):
    if callback_query.data == 'stats_active':
        # يتم زيادة عدد المستخدمين النشطين وعرض الرسالة
        stats['active_users'] += 1
        callback_query.answer(f"تم اختيار المستخدمين النشطين ({stats['active_users']})")
        callback_query.edit_message_text("تم اختيار المستخدمين النشطين.")
    elif callback_query.data == 'stats_banned':
        # يتم زيادة عدد المستخدمين المحظورين وعرض الرسالة
        stats['banned_users'] += 1
        callback_query.answer(f"تم اختيار المستخدمين المحظورين ({stats['banned_users']})")
        callback_query.edit_message_text("تم اختيار المستخدمين المحظورين.")
