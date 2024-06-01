#
# Copyright (C) 2024-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#
import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from YukkiMusic.utils import seconds_to_min, time_to_seconds
from YukkiMusic.utils.channelplay import get_channeplayCB
from YukkiMusic.utils.database import is_video_allowed
from YukkiMusic.utils.decorators.language import languageCB
from YukkiMusic.utils.decorators.play import PlayWrapper
from YukkiMusic.utils.formatters import formats
from YukkiMusic.utils.inline.play import (
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from YukkiMusic.utils.inline.playlist import botplaylist_markup
from YukkiMusic.utils.logger import play_logs
from YukkiMusic.utils.stream.stream import stream

# Command
PLAY_COMMAND = get_command("PLAY_COMMAND")


@app.on_message(
    filters.command(
        [
            "play",
            "vplay",
            "cplay",
            "cute",
            "cvplay",
            "playforce",
            "vplayforce",
            "cplayforce",
            "cvplayforce",
        ],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    mystic = await message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id if message.from_user else "1121532100"
    user_name = message.from_user.first_name if message.from_user else None
    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    if audio_telegram:
        if audio_telegram.file_size > config.TG_AUDIO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_5"])
        duration_min = seconds_to_min(audio_telegram.duration)
        if (audio_telegram.duration) > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, duration_min)
            )
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }

            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif video_telegram:
        if not await is_video_allowed(message.chat.id):
            return await mystic.edit_text(_["play_3"])
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text(
                        _["play_8"].format(f"{' | '.join(formats)}")
                    )
            except:
                return await mystic.edit_text(
                    _["play_8"].format(f"{' | '.join(formats)}")
                )
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_9"])
        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(video_telegram)
            dur = await Telegram.get_duration(video_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }
            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    video=True,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif url:
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    print(e)
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]
                img = config.PLAYLIST_IMG_URL
                cap = _["play_10"]
            elif "https://youtu.be" in url:
                videoid = url.split("/")[-1].split("?")[0]
                details, track_id = await YouTube.track(url)
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
            else:
                details, track_id = await YouTube.track(url)
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text(
                    "ᴛʜɪs ʙᴏᴛ ᴄᴀɴ'ᴛ ᴩʟᴀʏ sᴩᴏᴛɪғʏ ᴛʀᴀᴄᴋs ᴀɴᴅ ᴩʟᴀʏʟɪsᴛs, ᴩʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ ᴀɴᴅ ᴀsᴋ ʜɪᴍ ᴛᴏ ᴀᴅᴅ sᴩᴏᴛɪғʏ ᴩʟᴀʏᴇʀ."
                )
            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spplay"
                img = config.SPOTIFY_PLAYLIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spalbum"
                img = config.SPOTIFY_ALBUM_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spartist"
                img = config.SPOTIFY_ARTIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
        elif await Apple.valid(url):
            apple = True
            if not config.APPLEMUSIC:
                return await mystic.edit_text(
                    "ᴛʜɪs ʙᴏᴛ ᴄᴀɴ'ᴛ ᴩʟᴀʏ ᴀᴘᴩʟᴇ ᴍᴜsɪᴄ ᴛʀᴀᴄᴋs ᴀɴᴅ ᴩʟᴀʏʟɪsᴛs, ᴩʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ ᴀɴᴅ ᴀsᴋ ʜɪᴍ ᴛᴏ ᴀᴅᴅ ᴀᴩᴩʟᴇ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ."
                )
            if "track" in url:
                try:
                    details, track_id = await Apple.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Apple.playlist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spplay"
                img = config.APPLEMUSIC_PLAYLIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "album" in url:
                try:
                    details, plist_id = await Apple.album(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spalbum"
                img = config.APPLEMUSIC_ALBUM_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "artist" in url:
                try:
                    details, plist_id = await Apple.artist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spartist"
                img = config.APPLEMUSIC_ARTIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
        elif await SoundCloud.exists(url):
            if "playlist" in url:
                try:
                    details = await SoundCloud.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    print(e)
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "sc"
                if "&" in url:
                    plist_id = (url.split("/")[-1]).split("&")[0]
                else:
                    plist_id = url.split("/")[-1]
                img = config.PLAYLIST_IMG_URL
                cap = _["play_10"]
            else:
                details, track_id = await SoundCloud.track(url)
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
        elif await Resso.exists(url):
            if "playlist" in url:
                try:
                    details = await Resso.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    print(e)
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "rs"
                if "&" in url:
                    plist_id = (url.split("/")[-1]).split("&")[0]
                else:
                    plist_id = url.split("/")[-1]
                img = config.PLAYLIST_IMG_URL
                cap = _["play_10"]
            else:
                details, track_id = await Resso.track(url)
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
        else:
            return await mystic.edit_text(_["play_3"])
        try:
            track = {
                "details": details,
                "channel": channel,
                "img": img,
                "plist_id": plist_id,
                "plist_type": plist_type,
                "slider": slider,
                "user_id": user_id,
                "user_name": user_name,
                "video": video,
                "spotify": spotify,
                "apple": apple,
                "channel": channel,
                "url": url,
                "streamtype": streamtype,
                "cap": cap,
                "forceplay": fplay,
            }
            await play_logs(
                message, message.chat.id, user_id, details, user_name, streamtype
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            return await mystic.edit_text(err)
        try:
            await get_channeplayCB(
                app,
                channel,
                user_id,
                track,
                message.chat.id,
            )
        except NoActiveGroupCall:
            await mystic.edit_text(_["play_7"])
        return await mystic.delete()
