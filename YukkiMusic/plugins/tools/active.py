#
# Copyright (C) 2024-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import Message
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database.memorydatabase import (
    get_active_chats,
    get_active_video_chats,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import SUPPORT_CHANNEL  
from strings.filters import command

@app.on_message(command(["⦗ الاتصالات النشطة  ⦘", "الاتصالات النشطة"]))
async def active_chats(_, message: Message):
    if message.from_user.id not in SUDOERS:
        return await message.reply_text(
            "عذرًا، هذا الأمر مخصص للمطور فقط -"
        )

    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("⦗ قناة التحديثات ⦘", url=SUPPORT_CHANNEL)],
        ]
    )

    # إرسال الرد مع الزر الشفاف
    await message.reply_text(
        f"-› عزيزي المطور هذا هي اتصالات المجموعات التي يجرى تشغيل حساب المساعد فيها : \n\n
-› الصوت {ac_audio}\n-› الفيديو : {ac_video}",
        reply_markup=keyboard,
    )
