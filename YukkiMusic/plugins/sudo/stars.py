import asyncio
import platform
from sys import version as pyver

import psutil
from ntgcalls import __version__ as ngtgver
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message
import config
from YukkiMusic import app
from YukkiMusic.core.userbot import assistants
from YukkiMusic.misc import SUDOERS
from YukkiMusic.plugins import ALL_MODULES
from YukkiMusic.utils.database import get_served_chats, get_served_users, get_queries, get_sudoers


@app.on_message(filters.command("stats"))
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
    total_queries = await get_queries()
    blocked = len(config.BANNED_USERS)
    sudoers = len(SUDOERS)
    modules = len(ALL_MODULES)
    assistant_count = len(assistants)
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    play_duration = config.DURATION_LIMIT_MIN
    auto_leaving = "Yes" if config.AUTO_LEAVING_ASSISTANT else "No"

    # Formatting the message
    stats_message = f"""
**Bot Statistics and Information:**

**System Information:**
- Platform: {sc}
- Physical Cores: {p_core}
- Total Cores: {t_core}
- RAM: {ram}
- Disk Total: {total}
- Disk Used: {used}
- Disk Free: {free}

**Bot Information:**
- Served Chats: {served_chats}
- Served Users: {served_users}
- Total Queries: {total_queries}
- Blocked Users: {blocked}
- Sudo Users: {sudoers}
- Modules: {modules}
- Assistants: {assistant_count}

**Bot Settings:**
- Playlist Limit: {playlist_limit}
- Fetch Playlist Limit: {fetch_playlist}
- Play Duration Limit: {play_duration} mins
- Auto Leaving Assistant: {auto_leaving}

**Software Versions:**
- Python Version: {pyver.split()[0]}
- Pyrogram Version: {pyrover}
- Py-TgCalls Version: {pytgver}
- N-TgCalls Version: {ngtgver}
"""

    # Sending the statistics message
    await message.reply_text(stats_message)
