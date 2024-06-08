from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import platform
import socket
import psutil
import re
from YukkiMusic import app
import requests
import speedtest
import datetime
import os
import uuid
from strings.filters import command
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

# دالة للحصول على نوع الاستضافة
def get_hosting_type():
    if "DYNO" in os.environ:
        return "Heroku"
    elif "PYTHONHOME" in os.environ:
        return "PythonAnywhere"
    elif "LD_LIBRARY_PATH" in os.environ:
        return "Linux VPS"
    else:
        return "غير معروف"

# دالة للتحقق من حالة الشبكة
def check_internet_connection():
    try:
        requests.get("https://www.google.com/", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# دالة للحصول على حالة الشبكة
def get_network_status():
    if check_internet_connection():
        return "متصل بالإنترنت"
    else:
        return "غير متصل بالإنترنت"

# دالة للحصول على معلومات الشبكة
def get_network_information():
    try:
        # العنوان IP العام
        public_ip = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", requests.get("https://api64.ipify.org").text).group(0)
    except Exception as e:
        public_ip = "غير متاح"

    # اسم مزود خدمة الإنترنت
    try:
        isp_name = requests.get("https://ipinfo.io/org").text.strip()
    except Exception as e:
        isp_name = "غير متاح"


# دالة للحصول على وقت تشغيل البوت
start_time = datetime.datetime.now()

def get_uptime():
    uptime = datetime.datetime.now() - start_time
    return str(uptime).split(".")[0]

# دالة للحصول على معلومات الذاكرة الفعلية المستخدمة
def get_actual_used_memory():
    used_memory = psutil.virtual_memory().used
    return humanbytes(used_memory)

# دالة للحصول على معلومات الحمولة الحالية للمعالج
def get_cpu_load():
    cpu_load = psutil.cpu_percent(interval=1)
    return f"{cpu_load}%"

# دالة للحصول على معلومات الذاكرة والحمولة للمعالج
def get_system_info():
    # معلومات الذاكرة
    virtual_memory = psutil.virtual_memory()
    total_memory = humanbytes(virtual_memory.total)
    available_memory = humanbytes(virtual_memory.available)
    used_memory = humanbytes(virtual_memory.used)
    percent_memory = virtual_memory.percent

    # معلومات الحمولة للمعالج
    cpu_percent = psutil.cpu_percent(interval=1)

    return total_memory, available_memory, used_memory, percent_memory, cpu_percent

# أمر sysinfo لعرض معلومات النظام
@app.on_message(command(["⦗ معلومات النظام ⦘", "النظام"]) & (filters.private | filters.group))
async def fetch_system_information(client, message):
    if message.from_user.id != OWNER:
        await message.reply_text("هذا الامر يخص المطور الأساسي فقط.")
        return

    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    cpu_len = len(psutil.Process().cpu_affinity())

    hosting_type = get_hosting_type()

    public_ip, isp_name, speed_info = get_network_information()

    uptime = get_uptime()

    total_memory, available_memory, used_memory, percent_memory, cpu_percent = get_system_info()

    actual_used_memory = get_actual_used_memory()

    cpu_load = get_cpu_load()

    network_status = get_network_status()

    somsg = f"""
- نظام التشغيل : {splatform}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- إصدار نظام التشغيل : {platform_release}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- نسخة نظام التشغيل : {platform_version}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- اسم الجهاز : {hostname}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- عنوان IP : {ip_address}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- المعالج : {processor}
⎯ ⎯ ⎯ ⎯ ⎯ ⎯ ⎯ 
- اجمالي الذاكرة : {total_memory}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- المتاح : {available_memory}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- المستخدم : {used_memory} والمتبقي : ({percent_memory}%) 
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- الذاكرة الفعلية المستخدمة : {actual_used_memory}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- وحدة المعالجة المركزية : {cpu_load}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- الاستضافة : {hosting_type}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- حالة الشبكة : {network_status}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- العنوان IP العام : {public_ip}
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- وقت التشغيل : {uptime} س
⎯ ⎯ ⎯ ⎯⎯ ⎯ ⎯ 
- مطور السورس : [Freedom Source]({t.me/RR8R9})
"""

    # إنشاء زر شفاف
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⦗ قناة التحديثات ⦘", url=SUPPORT_CHANNEL)]]
    )

    await message.reply_text(
        text=somsg,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
