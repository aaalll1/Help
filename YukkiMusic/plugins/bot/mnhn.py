from YukkiMusic import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [ " **➠ تصبح على خير 🌚** ",
           " **➠ نام بهدوء 🙊** ",
           " **➠ ضع الهاتف ونام، وإلا سيأتيك شبح..👻** ",
           " **➠ أيها الحبيب نام في النهار، الآن نم..?? 🥲** ",
           " **➠ أمي، انظر إلى ابنك يتحدث مع صديقته تحت البطانية، لا يريد النوم 😜** ",
           " **➠ أبي، انظر إلى ابنك ما زال يستخدم الهاتف في الليل 🤭** ",
           " **➠ عزيزي، الليلة نخطط لأمسية رومانسية..?? 🌠** ",
           " **➠ تصبح على خير، اعتن بنفسك.. 🙂** ",
           " **➠ تصبح على خير وأحلام سعيدة..?? ✨** ",
           " **➠ الليل تأخر، نم..?? 🌌** ",
           " **➠ أمي، انظر الساعة الحادية عشرة وما زال يستخدم الهاتف، لا يريد النوم 🕦** ",
           " **➠ هل ستذهب إلى المدرسة غداً، لماذا ما زلت مستيقظاً 🏫** ",
           " **➠ حبيبي، تصبح على خير، اعتن بنفسك..?? 😊** ",
           " **➠ الجو بارد جداً اليوم، نم باكراً واستمتع بالدفء 🌼** ",
           " **➠ حبيبي، تصبح على خير 🌷** ",
           " **➠ سأذهب للنوم، تصبح على خير، اعتن بنفسك 🏵️** ",
           " **➠ مرحباً، تصبح على خير 🍃** ",
           " **➠ عزيزي، هل لم تنم بعد ☃️** ",
           " **➠ تصبح على خير، الليل تأخر..? ⛄** ",
           " **➠ سأذهب للنوم، تصبح على خير 😁** ",
           " **➠ تصبح على خير، لا تنساني، سأذهب للنوم 🌄** ",
           " **➠ تصبح على خير، وأحلام سعيدة ❤️** ",
           " **➠ تصبح على خير، لا تنسى الابتسام 💚** ",
           " **➠ تصبح على خير، أنام الآن 🥱** ",
           " **➠ تصبح على خير يا صديقي 💤** ",
           " **➠ حبيبي، الليلة نخطط لأمسية رومانسية 🥰** ",
           " **➠ لماذا ما زلت مستيقظاً، هل لم تنم بعد 😜** ",
           " **➠ أغلق عينيك، والتزم بالهدوء، الملائكة ستراقبك الليلة... 💫** ",
           ]

VC_TAG = [ "**➠ صباح الخير، كيف حالك 🐱**",
         "**➠ صباح الخير، استيقظ 🌤️**",
         "**➠ صباح الخير يا حبيبي، اشرب الشاي ☕**",
         "**➠ استيقظ، هل لن تذهب إلى المدرسة اليوم 🏫**",
         "**➠ استيقظ بسرعة، وإلا سأصب الماء عليك 🧊**",
         "**➠ حبيبي، استيقظ واغتسل، الإفطار جاهز 🫕**",
         "**➠ هل لن تذهب إلى العمل اليوم، ما زلت نائماً 🏣**",
         "**➠ صباح الخير، ماذا ستشرب قهوة أم شاي ☕🍵**",
         "**➠ حبيبي، الساعة الثامنة وأنت ما زلت نائماً 🕖**",
         "**➠ استيقظ أيها الكسول... ☃️**",
         "**➠ صباح الخير، يوم سعيد... 🌄**",
         "**➠ صباح الخير، أتمنى لك يوماً سعيداً... 🪴**",
         "**➠ صباح الخير، كيف حالك حبيبي 😇**",
         "**➠ أمي، انظر هذا النائم لم يستيقظ بعد... 😵‍💫**",
         "**➠ هل كنت نائماً طوال الليل، لماذا ما زلت نائماً... 😏**",
         "**➠ حبيبي، استيقظ وقل صباح الخير لأصدقائك في المجموعة... 🌟**",
         "**➠ أبي، هذا النائم لم يستيقظ بعد، المدرسة على وشك البدء... 🥲**",
         "**➠ حبيبي، صباح الخير، ماذا تفعل ... 😅**",
         "**➠ صباح الخير يا صديقي، هل تناولت الإفطار... 🍳**",
        ]

@app.on_message(filters.command(["gntag"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ هذه الأوامر فقط للمجموعات.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ أنت لست مسؤولاً، فقط المسؤولين يمكنهم مناداة الأعضاء. ")

    if message.reply_to_message and message.text:
        return await message.reply("/tagall اكتب صباح الخير أو قم بالرد على رسالة للتنبيه...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/tagall اكتب صباح الخير أو قم بالرد على رسالة للتنبيه...")
    else:
        return await message.reply("/tagall اكتب صباح الخير أو قم بالرد على رسالة للتنبيه...")
    if chat_id in spam_chats:
        return await message.reply("๏ أوقف التنبيه أولاً...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{random.choice(TAGMES)}\n\n{usrtxt}\n\n"
                txt += random.choice(EMOJI)
                await client.send_message(chat_id, txt)
                await asyncio.sleep(1)
                usrnum = 0
                usrtxt = ""
            elif mode == "text_on_reply":
                await msg.reply(f"{usrtxt}")
                await asyncio.sleep(1)
                usrnum = 0
                usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(filters.command(["mntag"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ هذه الأوامر فقط للمجموعات.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ أنت لست مسؤولاً، فقط المسؤولين يمكنهم مناداة الأعضاء.")

    if message.reply_to_message and message.text:
        return await message.reply("/tagall اكتب صباح الخير أو قم بالرد على رسالة للتنبيه...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/tagall اكتب صباح الخير أو قم بالرد على رسالة للتنبيه...")
    else:
        return await message.reply("/tagall اكتب صباح الخير أو قم بالرد على رسالة للتنبيه...")
    if chat_id in spam_chats:
        return await message.reply("๏ أوقف التنبيه أولاً...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{random.choice(VC_TAG)}\n\n{usrtxt}\n\n"
                txt += random.choice(EMOJI)
                await client.send_message(chat_id, txt)
                await asyncio.sleep(1)
                usrnum = 0
                usrtxt = ""
            elif mode == "text_on_reply":
                await msg.reply(f"{usrtxt}")
                await asyncio.sleep(1)
                usrnum = 0
                usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass
