from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER, START_IMG_URL

# Dummy function add_served_user to avoid error
async def add_served_user(user_id: int):
    # You can add user storage logic here if necessary
    pass

# Command handlers
@app.on_message(filters.command(["start", "help"]) & filters.private)
async def start_(c: Client, message: Message):
    user_id = message.from_user.id
    await add_served_user(user_id)
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⦗ اوامر البوت ⦘", callback_data="command_list")
                ],
                [
                    InlineKeyboardButton(text="⦗ قناة السورس ⦘", url=SUPPORT_CHANNEL),
                    InlineKeyboardButton(text="⦗ قناة التحديثات ⦘", url=SUPPORT_GROUP),
                ],
                [
                    InlineKeyboardButton(text="⦗ مطور البوت ⦘", user_id=int(OWNER)),
                ],
            ]
        )
    )

# Callback query handlers
@app.on_callback_query(filters.regex("home_start"))
async def start_set(_, query: CallbackQuery):
    await query.answer("القائمة الرئيسية")
    await query.edit_message_text(
        f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⦗ اوامر البوت ⦘", callback_data="command_list")
                ],
                [
                    InlineKeyboardButton(text="⦗ قناة السورس ⦘", url=SUPPORT_CHANNEL),
                    InlineKeyboardButton(text="⦗ قناة التحديثات ⦘", url=SUPPORT_GROUP),
                ],
                [
                    InlineKeyboardButton(text="⦗ مطور البوت ⦘", user_id=int(OWNER)),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("command_list"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("👍🏻قائمة الاوامر")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر التشغيل ⦘", callback_data="user_command"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next_admin"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next_admin"))
async def next_admin_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم لأوامر المطورين")
    await query.edit_message_text(
        """- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر المطورين ⦘", callback_data="developer_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="command_list"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next_user"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("developer_commands"))
async def developer_commands_set(_, query: CallbackQuery):
    await query.answer("اوامر المطورين")
    await query.edit_message_text(
        f"""اوامر المطورين ↓""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next_user"),
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("next_user"))
async def next_user_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم لأوامر الادمن")
    await query.edit_message_text(
        """- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر الادمن ⦘", callback_data="admin_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="developer_commands_info"),
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("admin_commands"))
async def admin_commands_set(_, query: CallbackQuery):
    await query.answer("اوامر الادمن")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر الادمن ⦘", callback_data="admin_commands"),                    
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="next_user"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="developer_commands_info"),
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("user_command"))
async def user_commands_set(_, query: CallbackQuery):
    await query.answer("اوامر التشغيل")
    await query.edit_message_text(
        f"""اوامر التشغيل""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="developer_commands_info")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("developer_commands_info"))
async def developer_commands_info_set(_, query: CallbackQuery):
    await query.answer("المزيد من المعلومات حول أوامر المطورين")
    await query.edit_message_text(
        f"""المزيد من المعلومات حول أوامر المطورين""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="admin_commands")
                ],
            ]
        ),
    )
