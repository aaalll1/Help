from pyrogram import filters, Client
from YukkiMusic import app
import asyncio
import config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import InputStream, AudioParameters, AudioVideoParameters
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import *
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, AlreadyJoinedError

@app.on_message(filters.regex("^الصاعدين$"))
async def strcall(client, message):
    assistant = await group_assistant(Dil, message.chat.id)
    try:
        await assistant.join_group_call(
            message.chat.id,
            InputStream(
                AudioPiped("https://graph.org/file/217aac5f9cd2b05f7ba5a.mp4"),
                AudioParameters(
                    bit_rate=64000
                )
            ),
            stream_type=StreamType().pulse_stream
        )
        text = "-› الصاعدين بالأتصال :\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k = 0
        for participant in participants:
            info = participant
            mut = "-› جاي يسولف " if not info.muted else "-› ساد المايك "
            user = await client.get_users(participant.user_id)
            k += 1
            text += f"{k} -› {user.mention} {mut}\n"
        text += f"\n-› عددهم : {len(participants)}\n️"

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⦗ قناة التحديثات ⦘", url=config.SUPPORT_CHANNEL)],
        ])      

        await message.reply(f"{text}", reply_markup=inline_keyboard)
        await asyncio.sleep(7)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply(f"-› ماكو شي مشتغل")
    except TelegramServerError:
        await message.reply(f"- حدث خطأ.")
    except AlreadyJoinedError:
        text = "-› الصاعدين :\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k = 0
        for participant in participants:
            info = participant
            mut = "-› جاي يسولف " if not info.muted else "-› ساد المايك "
            user = await client.get_users(participant.user_id)
            k += 1
            text += f"{k} ~ {user.mention} {mut}\n"
        text += f"\n-› عددهم : {len(participants)}\n️"

        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⦗ قناة التحديثات ⦘ ", url=config.SUPPORT_CHANNEL)],
        ])
        await message.reply(f"{text}", reply_markup=inline_keyboard)
