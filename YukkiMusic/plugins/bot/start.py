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


@app.on_callback_query(filters.regex("next"))
async def next_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم")
    await query.edit_message_text(
        """- تابع الازرار في الاسفل ↓

يمديك تشوف كل اوامر البوت عن طريق إستخدام الأزرار أدناه .""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر المطورين ⦘", callback_data="admin_commands"),
                    InlineKeyboardButton("⦗ اوامر المالك ⦘", callback_data="developer_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="command_list"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="command_list"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("user_command"))
async def guide_set(_, query: CallbackQuery):
    await query.answer("اوامر التشغيل")
    await query.edit_message_text(
        f"""طريقة التشغيل ، تابع في الاسفل ↓

1-› أولا ، أضفني الى مجموعتك
2-› بعد ذالك قم برفعي كمشرف واعطائي صلاحيات مثل باقي البشر.
3-› بعد ذالك اكتب `.تحديث` بيانات البوت
3-› اضف سيدي ومولاي في مجموعتك او اكتب `.انضم` لدعوة المساعد
4-› اذ لم تستطيع اضافة المساعد او واجهت مشاكل تحدث مع رئيس الوزراء  .

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("admin_commands"))
async def guide_set(_, query: CallbackQuery):
    await query.answer("اوامر الادمن")
    await query.edit_message_text(
        f"""اوامر الادمن""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="next")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("developer_commands"))
async def guide_set(_, query: CallbackQuery):
    await query.answer("اوامر المطورين")
    await query.edit_message_text(
        f"""اوامر المطورين ↓

1-› أولا ، أضفني الى مجموعتك
2-› بعد ذالك قم برفعي كمشرف واعطائي صلاحيات مثل باقي البشر.
3-› بعد ذالك اكتب `.تحديث` بيانات البوت
3-› اضف سيدي ومولاي في مجموعتك او اكتب `.انضم` لدعوة المساعد
4-› اذ لم تستطيع اضافة المساعد او واجهت مشاكل تحدث مع رئيس الوزراء  .

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ رجوع ⦘", callback_data="next")
                ],
            ]
        ),
    )
