from pyrogram import Client, filters
from driver.filters import command2
from driver.decorators import authorized_users_only
from driver.veez import user as USER
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from config import UPDATES_CHANNEL, FORCE_SUBSCRIBE_TEXT, SUBSCRIBE

@Client.on_message(command2(["القناة المرتبطه"]) & ~filters.private & ~filters.bot)
@authorized_users_only
async def ch_id(client, message):
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
    try:
      get = await client.get_chat(message.chat.id)
      getch = get.linked_chat
    except:
      await message.reply_text("المجموعة غير مرتبطه بي اي قناة")
      return
    text = f"""معلومات القناة المرتبطه
الاسم : {getch.title}
المعرف : {getch.username}
الايدي : {getch.id}"""
    await message.reply_text(text)

@Client.on_message(command2(["القناة انضم"]) & ~filters.private & ~filters.bot)
@authorized_users_only
async def ch_join(client, message):
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
    try:
       get = await client.get_chat(message.chat.id)
       getch = get.linked_chat
    except:
       await message.reply_text("المجموعة غير مرتبطه بي اي قناة")
       return
    try:
       invite = await client.export_chat_invite_link(getch.id)
    except:
       await message.reply_text("البوت ليس ادمن في القناة او لا يمتلك صلاحية دعوة المستخدمين")
       return
    try:
       await USER.join_chat(invite)
       await message.reply_text("الحساب المساعد نجح في الانضمام الي القناة " + getch.title)
    except UserAlreadyParticipant:
       await message.reply_text("الحساب المساعد بالفعل في القناة الخاصة بك الخاصة بك")
    except Exception as e:
       await message.reply_text(f"فشل الحساب المساعد في الانضمام \n الخطأ : {e}")
       return
