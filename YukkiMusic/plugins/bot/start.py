from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER, START_IMG_URL

# دالة وهمية add_served_user لتجنب الخطأ
async def add_served_user(user_id: int):
    # يمكنك إضافة منطق تخزين المستخدم هنا إذا لزم الأمر
    pass

@app.on_message(
    filters.command(["start", "help"]) & filters.private
)
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
    user_id = query.from_user.id
    await query.answer("👍🏻قائمة الاوامر")
    await query.edit_message_text(
        f"""- تابع الازرار في الاسفل ↓

يمديك تشوف كل اوامر البوت عن طريق إستخدام الأزرار أدناه .""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر التشغيل ⦘", callback_data="user_command"),
                ],
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="developer_commands"),
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="home_start"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("developer_commands"))
async def developer_commands_set(_, query: CallbackQuery):
    await query.answer("اوامر المطورين")
    await query.edit_message_text(
        f"""- تابع الازرار في الاسفل ↓

يمديك تشوف كل اوامر البوت عن طريق إستخدام الأزرار أدناه .""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر الادمن ⦘", callback_data="admin_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="command_list"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="admin_commands"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("admin_commands"))
async def admin_commands_set(_, query: CallbackQuery):
    await query.answer("اوامر الادمن")
    await query.edit_message_text(
        f"""- تابع الازرار في الاسفل ↓

يمديك تشوف كل اوامر البوت عن طريق إستخدام الأزرار أدناه .""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="command_list"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("user_command"))
async def user_commands_set(_, query: CallbackQuery):
    await query.answer("اوامر التشغيل")
    await query.edit_message_text(
        f"""- تابع الازرار في الاسفل ↓

يمديك تشوف كل اوامر البوت عن طريق إستخدام الأزرار أدناه .""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="command_list"),
                ],
            ]
        ),
    )
