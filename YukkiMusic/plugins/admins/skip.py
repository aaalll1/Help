from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, ChatWriteForbidden
from strings.filters import command
import config
from config import BANNED_USERS, Muntazer
from YukkiMusic import YouTube, app
from YukkiMusic.core.call import Yukki
from YukkiMusic.misc import db
from YukkiMusic.utils.database import get_loop
from YukkiMusic.utils.decorators import AdminRightsCheck
from YukkiMusic.utils.inline.play import stream_markup, telegram_markup
from YukkiMusic.utils.stream.autoclear import auto_clean
from YukkiMusic.utils.thumbnails import gen_thumb


@app.on_message(command(["تخطي", "cnext"]) & ~BANNED_USERS)
@AdminRightsCheck
async def skip_command(cli, message: Message):
    chat_id = message.chat.id
    if not Muntazer:
        return
    try:
        if message.from_user is None:
            return

        await cli.get_chat_member(Muntazer, message.from_user.id)
    except UserNotParticipant:
        if Muntazer.isalpha():
            link = "https://t.me/" + Muntazer
        else:
            chat_info = await cli.get_chat(Muntazer)
            link = chat_info.invite_link
        await message.reply(
            f"~︙عزيزي {message.from_user.mention} \n~︙عليك الأشتراك في قناة البوت \n~︙قناة البوت : @{Muntazer}.",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("< Source Plus >", url=link)]
            ])
        )
        return

    try:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(_["admin_8"])

        check = db.get(chat_id)
        if not check:
            return await message.reply_text(_["queue_2"])

        popped = check.pop(0)
        if popped:
            await auto_clean(popped)
        if not check:
            await message.reply_text(
                text=_["admin_6"].format(
                    message.from_user.mention, message.chat.title
                ),
                reply_markup=close_markup(_),
            )
            try:
                return await Yukki.stop_stream(chat_id)
            except:
                return

        queued = check[0]["file"]
        title = check[0]["title"].title()
        user = check[0]["by"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None

        db[chat_id][0]["played"] = 0
        exis = check[0].get("old_dur")
        if exis:
            db[chat_id][0]["dur"] = exis
            db[chat_id][0]["seconds"] = check[0]["old_second"]
            db[chat_id][0]["speed_path"] = None
            db[chat_id][0]["speed"] = 1.0

        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await message.reply_text(_["admin_7"].format(title))
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
            try:
                await Yukki.skip_stream(chat_id, link, video=status, image=image)
            except:
                return await message.reply_text(_["call_6"])
            button = stream_markup(_, chat_id)
            img = await get_thumb(videoid)
            run = await message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:23],
                    check[0]["dur"],
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif "vid_" in queued:
            mystic = await message.reply_text(_["call_7"], disable_web_page_preview=True)
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=status,
                )
            except:
                return await mystic.edit_text(_["call_6"])
            try:
                image = await YouTube.thumbnail(videoid, True)
            except:
                image = None
            try:
                await Yukki.skip_stream(chat_id, file_path, video=status, image=image)
            except:
                return await mystic.edit_text(_["call_6"])
            button = stream_markup(_, chat_id)
            img = await get_thumb(videoid)
            run = await message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    title[:23],
                    check[0]["dur"],
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await mystic.delete()
        elif "index_" in queued:
            try:
                await Yukki.skip_stream(chat_id, videoid, video=status)
            except:
                return await message.reply_text(_["call_6"])
            button = stream_markup(_, chat_id)
            run = await message.reply_photo(
                photo=config.STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            if videoid == "telegram":
                image = None
            elif videoid == "soundcloud":
                image = None
            else:
                try:
                    image = await YouTube.thumbnail(videoid, True)
                except:
                    image = None
            try:
                await Yukki.skip_stream(chat_id, queued, video=status, image=image)
            except:
                return await message.reply_text(_["call_6"])
            if videoid == "telegram":
                button = stream_markup(_, chat_id)
                run = await message.reply_photo(
                    photo=config.TELEGRAM_AUDIO_URL
                    if str(streamtype) == "audio"
                    else config.TELEGRAM_VIDEO_URL,
                    caption=_["stream_1"].format(
                        config.SUPPORT_CHANNEL, title[:23], check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = stream_markup(_, chat_id)
                run = await message.reply_photo(
                    photo=config.SOUNCLOUD_IMG_URL
                    if str(streamtype) == "audio"
                    else config.TELEGRAM_VIDEO_URL,
                    caption=_["stream_1"].format(
                        config.SUPPORT_CHANNEL, title[:23], check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                button = stream_markup(_, chat_id)
                img = await get_thumb(videoid)
                run = await message.reply_photo(
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat {Muntazer}!")
