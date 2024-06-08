from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import platform
import socket
import psutil
import re
from strings.filters import command
import uuid
from YukkiMusic import app
import os
from config import OWNER, SUPPORT_CHANNEL

# دالة لتحويل البايتات إلى صيغة قراءة بشرية
def humanbytes(B):
    """تحويل بايتات إلى قراءة بشرية"""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return "{0} {1}".format(B, "Bytes" if 0 == B > 1 else "Byte")
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B / GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B / TB)

# أمر sysinfo لعرض معلومات النظام
@app.on_message(command(["⦗ معلومات النظام ⦘", "النظام"]))
async def fetch_system_information(client, message):
    if message.from_user.id != OWNER:
        await message.reply_text("هذا الامر يخص المطور الأساسي فقط .")
        return

    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)} GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)} MHz"
    du = psutil.disk_usage(".")
    disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} ({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())

    # تحديد نوع الاستضافة
    if "DYNO" in os.environ:
        hosting_type = "Heroku"
    elif "PYTHONHOME" in os.environ:
        hosting_type = "PythonAnywhere"
    elif platform.system() == "Linux":
        hosting_type = "Linux VPS"
    else:
        hosting_type = "غير معروف"

    somsg = f"""🖥 **معلومات النظام**

**نظام التشغيل :** `{splatform}`
**إصدار نظام التشغيل :** `{platform_release}`
**نسخة نظام التشغيل :** `{platform_version}`
**المعمارية :** `{architecture}`
**اسم الجهاز :** `{hostname}`
**عنوان IP :** `{ip_address}`
**عنوان MAC :** `{mac_address}`
**المعالج :** `{processor}`
**الذاكرة العشوائية (RAM) :** `{ram}`
**عدد معالجات الـ CPU :** `{cpu_len}`
**تردد الـ CPU :** `{cpu_freq}`
**مساحة القرص :** `{disk}`

📡 **قناة السورس :** [أنقر هنا]({SUPPORT_CHANNEL})

🌐 **الاستضافة :** `{hosting_type}`
"""

    # إنشاء زر شفاف
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("قناة البوت", url=SUPPORT_CHANNEL)]]
    )

    await message.reply_text(
        text=somsg,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
