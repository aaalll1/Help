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
@app.on_callback_query()
async def callback_handler(_, query: CallbackQuery):
    data = query.data

    # Check for the data and handle accordingly
    if data == "home_start":
        await home_start(query)
    elif data == "command_list":
        await command_list(query)
    elif data == "next":
        await next_(query)  # Changed to next_ to avoid conflict with Python keyword
    elif data == "user_command":
        await user_command(query)
    elif data == "developer_commands":
        await developer_commands(query)
    elif data == "owner_commands":
        await owner_commands(query)

async def edit_message(query: CallbackQuery, text: str, markup: InlineKeyboardMarkup):
    await query.answer()
    await query.edit_message_caption(caption=text, reply_markup=markup)

async def home_start(query: CallbackQuery):
    text = f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯"""
    markup = InlineKeyboardMarkup(
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
    await edit_message(query, text, markup)

async def command_list(query: CallbackQuery):
    text = f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘"""
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⦗ اوامر التشغيل ⦘", callback_data="user_command"),
            ],
            [
                InlineKeyboardButton("⦗ التالي ⦘", callback_data="next"),
            ],
        ]
    )
    await edit_message(query, text, markup)

async def next_(query: CallbackQuery):
    text = """- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘"""
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⦗ اوامر المطورين ⦘", callback_data="developer_commands"),
            ],
            [
                InlineKeyboardButton("⦗ التالي ⦘", callback_data="next"),
            ],
        ]
    )
    await edit_message(query, text, markup)

async def user_command(query: CallbackQuery):
    text = """هذه هي اوامر التشغيل"""
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⦗ التالي ⦘", callback_data="next")
            ],
        ]
    )
    await edit_message(query, text, markup)

async def developer_commands(query: CallbackQuery):
    text = """هذه هي اوامر المطورين"""
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⦗ اوامر المالك ⦘", callback_data="owner_commands"),
            ],
            [
                InlineKeyboardButton("⦗ الرئيسية ⦘", callback_data="home_start"),
            ],
        ]
    )
    await edit_message(query, text, markup)

async def owner_commands(query: CallbackQuery):
    text = """هذه هي اوامر المالك"""
    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⦗ رجوع ⦘", callback_data="developer_commands"),
            ],
        ]
    )
   
    await edit_message(query, text, markup)
