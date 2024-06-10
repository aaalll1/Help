from pyrogram import Client, filters
from pyrogram.types import Message
from YukkiMusic import app
from strings.filters import command
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


@app.on_message(command("احسب"))
def calculate_math(client, message):   
    expression = message.text.split("احسب ", 1)[1]
    
    try:        
        result = eval(expression.replace("×", "*").replace("÷", "/"))  # استبدال علامات الضرب والقسمة
        response = f"~ الناتج هو : {result}"
    except:
        response = "~ اكتب بالصيغة الصحيحة مثل: احسب 3 + 3 * 4"
        
    message.reply(response)

@app.on_message(
    command(["مبرمج السورس", "السورس", "المبرمج"])
)
async def maker(client: Client, message: Message):
    await message.reply_photo(
        photo="https://graph.org/file/0eca83858bc006e05b8dc.jpg",
        caption="~ Team freedom Arabi \n~ Dav Source",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⦗ Dev ⦘", url="https://t.me/RR8R9"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "⦗ Source channel ⦘", url="https://t.me/Xl444"
                    ),
                    InlineKeyboardButton(
                        "⦗ Updates channel ⦘", url="https://t.me/vvyvv6"
                    ),
                ],
            ]
        ),
    )
