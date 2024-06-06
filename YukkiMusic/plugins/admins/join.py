from pyrogram import filters
from pyrogram.errors import ChatAdminRequired, InviteRequestSent, UserAlreadyParticipant
from strings.filters import command
from YukkiMusic import app
from YukkiMusic.utils.database import get_assistant


@app.on_message(
    command(["انضم","ادخل","طب"]))
async def invite_assistant(client, message):
    try:
        # Get the music bot assistant
        userbot = await get_assistant(message.chat.id)

        # Check if the bot has admin rights in the group
        try:
            await client.get_chat_member(message.chat.id, "me")
        except ChatAdminRequired:
            return await message.reply_text(
                "• انطيني صلاحية اضافة مستخدمين ."
            )

        # Unban the assistant if it's banned in the group
        try:
            await client.unban_chat_member(message.chat.id, userbot.id)
        except:
            pass

        # Get the invite link for the group
        invitelink = await client.export_chat_invite_link(message.chat.id)

        # Invite the assistant to the group
        await userbot.join_chat(invitelink)

        await message.reply_text("-› تمت دعوة المساعد بنجاح .")

    except InviteRequestSent:
        await message.reply_text("-› بالفعل تم دعوة المساعد .")

    except UserAlreadyParticipant:
        await message.reply_text("-› المساعد موجود .")

    except Exception as e:
        await message.reply_text(f"-› حدث خطأ .: {e}")
