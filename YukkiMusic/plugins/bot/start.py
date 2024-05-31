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
        caption=f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه .""",
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
@app.on_callback_query()
async def callback_handler(_, query: CallbackQuery):
    # Handle callback queries based on data
    data = query.data

    if data == "home_start":
        await query.answer("القائمة الرئيسية")
        await query.edit_message_text(
            f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه .""",
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
    elif data == "command_list":
        await query.answer("👍🏻قائمة الاوامر")
        await query.edit_message_text(
            """- تم فتح لوحة التحكم ↓
 – – – – – – 
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
    elif data == "next":
        await query.answer("تم فتح لوحة التحكم")
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
                    ],
                ]
            )
        )
    elif data == "user_command":
        await query.answer("اوامر التشغيل")
        await query.edit_message_text(
            """هذا هي اوامر التشغيل""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⦗ التالي ⦘", callback_data="next")
                    ],
                ]
            ),
        )
    elif data == "developer_commands":
        await query.answer("اوامر المطورين")
        await query.edit_message_text(
            """هذا هي اوامر المطوربن""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⦗ رجوع ⦘", callback_data="next")
                    ],
                    [
                        InlineKeyboardButton("⦗ اوامر المالك ⦘", callback_data="owner_commands"),
                    ],
                ]
            ),
        )
    elif data == "owner_commands":
        await query.answer("اوامر المالك")
        await query.edit_message_text(
            """هذا هي اوامر المالك""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⦗ رجوع ⦘", callback_data="next")
                    ],
                ]
            ),
        )
