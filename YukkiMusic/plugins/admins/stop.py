#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant, ChatWriteForbidden, ChatAdminRequired
from YukkiMusic import app
from config import Muntazer
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import set_loop
from YukkiMusic.utils.decorators import AdminRightsCheck
from strings.filters import command
from config import BANNED_USERS
 
@app.on_message(filters.incoming & filters.private, group=-1) 
async def must_join_channel(app, msg):
    if not Muntazer:
        return
    try:
        if msg.from_user is None:
            return
        try:
            await app.get_chat_member(Muntazer, msg.from_user.id)
        except UserNotParticipant:
            if Muntazer.isalpha():
                link = "https://t.me/" + Muntazer
            else:
                chat_info = await app.get_chat(Muntazer)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    f"~︙عليك الأشتراك في قناة البوت \n~︙قناة البوت : @{Muntazer}.",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⦗ قناة الإشتراك ⦘", url=link)]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I m not admin in the MUST_JOIN chat {Muntazer}!")

 
# الكود لإيقاف الموسيقى  
@app.on_message(command(["ايقاف", "اوكف", "التالي", "انهاء"])) 
async def stop_music(cli, message: Message): 
    if not len(message.command) == 1: 
        return 
    # التحقق من الاشتراك في القناة 
    await must_join_channel(cli, message) 
    # إيقاف الموسيقى
    await Yukki.stop_stream(message.chat.id) 
    await set_loop(message.chat.id, 0) 
    # الرد على الرسالة بنجاح الإيقاف
    await message.reply_text( 
        _["admin_5"].format(message.from_user.first_name if message.from_user else 'Freedom'))
    )
