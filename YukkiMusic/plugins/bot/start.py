from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER, START_IMG_URL

# وهمي
async def add_served_user(user_id: int):
    pass

# متغير لتخزين كلمة البداية الجديدة
new_start_message = None

# يحدث عند كتابة "تغيير الكلمة الجديدة" للمطور
@app.on_message(filters.command("تغيير الكلمة الجديدة") & filters.user(OWNER))
async def change_start_message(_, message: Message):
    global new_start_message
    new_start_message = None  # تأكد من إعادة تعيينها
    await message.reply("أرسل كلمة البداية الجديدة لتحديثها.")

# يحدث عندما يرد المطور بكلمة البداية الجديدة
@app.on_message(filters.private & filters.user(OWNER) & ~filters.command)
async def set_new_start_message(_, message: Message):
    global new_start_message
    new_start_message = message.text
    await message.reply("تم تحديث كلمة البداية بنجاح!")

# عند كتابة "/start" أو "/help" من قبل أي مستخدم
@app.on_message(filters.command(["start", "help"]) & filters.private)
async def start_(c: Client, message: Message):
    global new_start_message
    user_id = message.from_user.id
    await add_served_user(user_id)
    
    # إذا كان هناك كلمة بداية جديدة، استخدمها، وإلا استخدم النص الأصلي
    if new_start_message:
        start_text = new_start_message
    else:
        start_text = f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯"""
    
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=start_text,
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

# تحديث رسالة البداية عند الضغط على "قائمة التحكم"
@app.on_callback_query(filters.regex("home_start"))
async def start_set(_, query: CallbackQuery):
    await query.answer("قائمة التحكم")
    global new_start_message
    start_text = new_start_message if new_start_message else f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯"""
    await query.edit_message_text(
        start_text,
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
