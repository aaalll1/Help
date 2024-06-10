import os
import glob
import asyncio
import time
from config import OWNER_ID
from YukkiMusic import app
from pyrogram import Client, filters

last_cleanup_time = 0
LOG_FILE = "cleanup_log.txt"
NOTIFICATION_FILE = "cleanup_notification.txt"

async def delete_temp_files():
    global last_cleanup_time
    while True:
        await asyncio.sleep(7200)  # انتظر ساعتين (7200 ثانية)

        current_time = time.time()

        if current_time - last_cleanup_time >= 7200:
            await clean_files()
            last_cleanup_time = current_time
            print("تم حذف الملفات بنجاح .")

@app.on_message(command(["⦗ تنظيف السجلات ⦘","تنظيف السجلات"], "") & filters.user(OWNER_ID))
async def clean(client: Client, message):
    global last_cleanup_time

    try:
        await message.delete()
    except:
        pass

    await clean_files()

    last_cleanup_time = time.time()
    await message.reply_text("-› تم حذف كافة الملفات .")

async def clean_files():
    downloads = os.path.realpath("downloads")

    if not os.path.exists(downloads):
        os.makedirs(downloads)

    down_dir = os.listdir(downloads)
    log_entries = []

    if down_dir:
        for file in down_dir:
            file_path = os.path.join(downloads, file)
            os.remove(file_path)
            log_entries.append(f"{time.ctime()}: Deleted {file_path}")

    files_to_delete = glob.glob("*.webm") + glob.glob("*.jpg") + glob.glob("*.png")
    for file_path in files_to_delete:
        os.remove(file_path)
        log_entries.append(f"{time.ctime()}: Deleted {file_path}")

    with open(LOG_FILE, 'a') as log_file:
        for entry in log_entries:
            log_file.write(entry + '\n')

    notification_path = os.path.join(downloads, NOTIFICATION_FILE)
    with open(notification_path, 'w') as notif_file:
        notif_file.write("تم حذف الملفات التالية:\n")
        for entry in log_entries:
            notif_file.write(entry + '\n')

# بدء عملية حذف الملفات بعد ساعتين
asyncio.ensure_future(delete_temp_files())
