import asyncio
from info import ASSISTANT_NAME
from config import SUDO_USERS, UPDATES_CHANNEL, FORCE_SUBSCRIBE_TEXT, SUBSCRIBE
from driver.decorators import authorized_users_only, sudo_users_only, errors
from driver.filters import command2, other_filters
from driver.veez import user as USER
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

@Client.on_message(command2(["انضم"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def join_group(client, message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", message.from_user.id)
           if not statusch.status:
              await message.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://t.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await message.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://t.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    if message.chat.username:
        invite = message.chat.username
    else:
        try:
             invite = await client.export_chat_invite_link(message.chat.id)
        except:
            await message.reply_text("• **ليس لدي صلاحية:**\n" + "\n» ⋆ __إضافة مستخدمين__")
            return

    try:
         await USER.join_chat(invite)
         await USER.send_message(
               chat_id=message.chat.id,
               text="✅ انضممت هنا كما طلبت",
               reply_to_message_id=message.message_id
               )
         await message.reply_text(f"✅ **تم دخول الحساب المساعد بنجاح**")
    except UserAlreadyParticipant:
          await USER.send_message(
          chat_id=message.chat.id,
          text="انا هنا بالفعل",
          reply_to_message_id=message.message_id
          )
          await message.reply_text("<b>الحساب المساعد بالفعل في الدردشة الخاصة بك</b>")
    except Exception as e:
          await message.reply_text(f"خطأ : {e}")
          return


@USER.on_message(command2(["غادر"]) & filters.group)
@authorized_users_only
async def leave_one(client, message):
    try:
        await message.reply_text("✅ قام الحساب المساعد بالخروج من المحادثة")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "⋆ **لن يستطيع الحساب المساعد الخروج لكثرة الطلبات.**\n\n**» برجاء طرده يدويا**"
        )

        return


@Client.on_message(command2(["مغادرة"]))
@sudo_users_only
async def leave_all(client, message):
    left = 0
    failed = 0
    lol = await message.reply("🔄 **يغادر البوت المساعد من المجموعات**!")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"الحساب المساعد يغادر جميع المجموعات...\n\nخرج من: {left} مجموعه.\nفشل : {failed} مجموعه."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"الحساب المساعد يغادر جميع المجموعات...\n\nخرج من: {left} مجموعه.\nفشل : {failed} مجموعه."
            )
    await client.send_message(
        message.chat.id, f"✅ تم الخروج من: {left} مجموعه.\n⋆ فشل: {failed} مجموعه."
    )
