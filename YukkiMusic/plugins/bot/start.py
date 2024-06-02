from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER, START_IMG_URL

# Variable to store the current start message
current_start_message = None

# وهمي
async def add_served_user(user_id: int):
    pass

@app.on_message(filters.command(["start", "help"]) & filters.private)
async def start_(c: Client, message: Message):
    user_id = message.from_user.id
    await add_served_user(user_id)
    global current_start_message
    if current_start_message:
        await current_start_message.delete()  # Delete the old start message
    current_start_message = await message.reply_photo(
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

# Command for the owner to update the start message
@app.on_message(filters.command("update_start") & filters.private & filters.user(int(OWNER)))
async def update_start_command(c: Client, message: Message):
    await message.reply("قم بإرسال رسالة الستارت الجديدة الآن.")

# Handler for the new start message sent by the owner
@app.on_message(filters.private & filters.user(int(OWNER)) & ~filters.command)
async def update_start_message(c: Client, message: Message):
    global current_start_message
    if current_start_message:
        await current_start_message.delete()  # Delete the old start message
    current_start_message = await message.reply(
        "تم حفظ رسالة الستارت الجديدة."
    )

# Callback query handlers
@app.on_callback_query(filters.regex("home_start"))
async def start_set(_, query: CallbackQuery):
    await query.answer("قائمة التحكم")
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

# Callback query handlers for navigation
@app.on_callback_query(filters.regex("command_list"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التشغيل")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ أوامر التشغيل ⦘", callback_data="user_command"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة الأدمن")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ أوامر الأدمن ⦘", callback_data="developer_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="command_list"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="ghaith"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("ghaith"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة المطور")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ اوامر المطور ⦘", callback_data="owner_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="command_list"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("user_command"))
async def user_commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح اوامر التشغيل")
    await query.edit_message_text(
        f"""هذا هي أوامر التشغيل
شغل 
تشغيل 

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("developer_commands"))
async def developer_commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح اوامر الأدمن")
    await query.edit_message_text(
        f"""هذه هيه اوامر المالك
        
        
منضر اوامر المالك

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="ghaith")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("owner_commands"))
async def owner_commands_set(_, query: CallbackQuery):
    await query.answer("تم فتح اوامر المطور")
    await query.edit_message_text(
        f"""هذه هيه اوامر المطور 

اذاعه مطور 

""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="home_start")
                ],
            ]
        ),
    )
