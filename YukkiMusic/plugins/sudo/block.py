from pyrogram import filters
from pyrogram.types import Message
from strings.filters import command
from config import BANNED_USERS
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import add_gban_user, remove_gban_user
from YukkiMusic.utils.decorators.language import language


@app.on_message(command(["حظر", "⦗ حظر عضو ⦘"]) & SUDOERS)
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("يرجى إرسال الإيدي أو اسم المستخدم لأقوم بحظره.")
    
    user = message.text.split(None, 1)[1]
    if "@" in user:
        user = user.replace("@", "")
    
    try:
        user = await app.get_users(user)
    except Exception as e:
        return await message.reply_text(f"لم أتمكن من العثور على المستخدم: {e}")

    if user.id in BANNED_USERS:
        return await message.reply_text(f"تم بالفعل حظر {user.mention if user.username is None else f'@{user.username}'}")

    await add_gban_user(user.id)
    BANNED_USERS.add(user.id)
    await message.reply_text(f"تم حظر {user.mention if user.username is None else f'@{user.username}'}")


@app.on_message(command(["الغاء حظر", "⦗ الغاء حظر عضو ⦘"]) & SUDOERS)
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("يرجى إرسال الإيدي أو اسم المستخدم لأقوم بإلغاء حظره.")
    
    user = message.text.split(None, 1)[1]
    if "@" in user:
        user = user.replace("@", "")
    
    try:
        user = await app.get_users(user)
    except Exception as e:
        return await message.reply_text(f"لم أتمكن من العثور على المستخدم: {e}")

    if user.id not in BANNED_USERS:
        return await message.reply_text("المستخدم غير محظور بالفعل")

    await remove_gban_user(user.id)
    BANNED_USERS.remove(user.id)
    await message.reply_text(f"تم إلغاء حظر {user.mention if user.username is None else f'@{user.username}'}")


@app.on_message(command(["المحظورين", "⦗ المحظورين ⦘"]) & SUDOERS)
@language
async def sudoers_list(client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text("لا يوجد مستخدمين محظورين")

    mystic = await message.reply_text("يتم البحث عن المستخدمين المحظورين...")
    msg = "قائمة المستخدمين المحظورين:\n\n"
    count = 0

    for user_id in BANNED_USERS:
        try:
            user = await app.get_users(user_id)
            user_mention = user.mention if user.username is None else f"@{user.username}"
            count += 1
        except Exception:
            continue

        msg += f"{count}. {user_mention} (ID: `{user_id}`)\n"

    if count == 0:
        return await mystic.edit_text("لا يوجد مستخدمين محظورين")

    else:
        return await mystic.edit_text(msg)
