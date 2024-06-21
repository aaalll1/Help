import asyncio
import platform
from sys import version as pyver
from datetime import datetime, timedelta
from strings.filters import command
import psutil
from ntgcalls import __version__ as ngtgver
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import config
from YukkiMusic import app
from YukkiMusic.core.userbot import assistants
from YukkiMusic.misc import SUDOERS
from YukkiMusic.plugins import ALL_MODULES
from YukkiMusic.utils.database import get_served_chats, get_served_users, get_active_users, get_sudoers

# Function to check if user is the owner
def is_owner(user_id):
    return user_id == config.OWNER_ID

# Function to get active chats
async def get_active_chats():
    # Logic to fetch active chats from database or wherever applicable
    active_chats = []  # Replace with your logic to fetch active chats
    return active_chats

@app.on_message(command(["احصائيات البوت", "⦗ احصائيات البوت ⦘"]) & filters.user(config.OWNER_ID))
async def stats(client, message: Message):
    # Collecting system information
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB"
    hdd = psutil.disk_usage("/")
    total = f"{round(hdd.total / (1024.0 ** 3), 2)} GB"
    used = f"{round(hdd.used / (1024.0 ** 3), 2)} GB"
    free = f"{round(hdd.free / (1024.0 ** 3), 2)} GB"

    # Collecting bot statistics
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    active_chats = len(await get_active_chats())
    active_users = len(await get_active_users())
    total_queries = await get_queries()
    blocked = len(config.BANNED_USERS)
    sudoers = len(SUDOERS)
    modules = len(ALL_MODULES)
    assistant_count = len(assistants)
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    play_duration = config.DURATION_LIMIT_MIN
    auto_leaving = "Yes" if config.AUTO_LEAVING_ASSISTANT else "No"

    # Calculate uptime
    uptime_seconds = round((datetime.now() - app.start_time).total_seconds())
    uptime = str(timedelta(seconds=uptime_seconds))

    # Channel link button
    SUPPORT_CHANNEL = config.SUPPORT_CHANNEL  # Assuming CHANNEL_LINK is defined in config.py

    # Inline keyboard markup
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⦗ قناة التحديثات ⦘", url=channel_link)]
        ]
    )

    # Formatting the message
    stats_message = f"""
**⦗ عزيزي المطور اليك احصائيات بوتك الحالي ⦘:**\n⎯ ⎯ ⎯ ⎯
-› إستضافتك : {sc}
-› عدد النوى : {p_core}
-› مجموع النوى : {t_core}
⎯ ⎯ ⎯ ⎯
-› عدد الكروبات : {served_chats}
-› الكروبات النشطة : {active_chats}
-› المستخدمين النشطين : {active_users}
-› عدد المستخدمين : {served_users}
⎯ ⎯ ⎯ ⎯
-› مجموع الأستعلامات : {total_queries}
-› المجموعات المبندة : {blocked}
-› عدد المطورين : {sudoers}
⎯ ⎯ ⎯ ⎯
-› المودلش : {modules}
-› عدد حسابات المساعد : {assistant_count}
-› اقصى مدة تشغيل : {play_duration} ثانية
⎯ ⎯ ⎯ ⎯
-› رام الاستضافة : {ram}
-› مغادرة التلقائية : {auto_leaving}
-› مدة تشغيل البوت : {uptime}
⎯ ⎯ ⎯ ⎯
-› إصدار نسخة البايثون : {pyver.split()[0]}
-› اصدار البايروجرام المستخدم : {pyrover}
-› إصدار الباي توجكلس : {ngtgver}
"""

    # Sending the statistics message with inline keyboard
    await message.reply_text(stats_message, reply_markup=keyboard)
