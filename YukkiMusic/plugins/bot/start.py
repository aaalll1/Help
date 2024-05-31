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
                ],[
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
        f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯\n\nقم بأضافة شيئا حتى تتمكن من اختصار امر""",
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
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر التشغيل ⦘", callback_data="user_command"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next"))
async def next_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر المطورين ⦘", callback_data="developer_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="command_list"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next1"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next1"))
async def next1_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ المالك ⦘", callback_data="owner_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="developer_commands"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next2"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next2"))
async def next2_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اخرى ⦘", callback_data="other_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="owner_commands"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next3"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next3"))
async def next3_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اخرى ⦘", callback_data="other_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="next2"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next4"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next4"))
async def next4_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اخرى ⦘", callback_data="other_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="next3"),
                    InlineKeyboardButton("⦗ العودة ⦘", callback_data="home_start"),
                ],
            ]
        )
    )
