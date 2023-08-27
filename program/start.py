from datetime import datetime
from sys import version_info
from time import time
from driver.veez import user as USER
from info import ASSISTANT_NAME, BOT_USERNAME
from config import (
    ALIVE_IMG,
    OWNER_NAME,
    UPDATES_CHANNEL,
    FORCE_SUBSCRIBE_TEXT,
    SUBSCRIBE,
    SUDO_USERS,
)
from driver.decorators import sudo_users_only
from program import __version__
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup
import speedtest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(command(["start"]) & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", message.from_user.id)
           if not statusch.status:
              await message.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة السورس", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await message.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة السورس", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    
    else:
        try:
           await message.reply_photo(
           photo=f"https://t.me/{BOT_USERNAME}",
           caption=f"""⋆ **مرحبا {message.from_user.mention()} **\n
⋆ **انا بوت استطيع تشغيل الموسيقي والفديو في محادثتك الصوتية
⋆ **تعلم طريقة تشغيلي واوامر التحكم بي عن طريق  » ⋆ الاوامر !**

⋆ **لتعلم طريقة تشغيلي بمجموعتك اضغط علي » ⋆اوامر اساسيه **
معرف الحساب المساعد @{ASSISTANT_NAME}""",
           reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("➕ أضفني لمجموعتك ➕",
                           url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                       )
                   ],
                   [InlineKeyboardButton("⋆ الاوامر الاساسيه", callback_data="cbhowtouse")],
                   [
                       InlineKeyboardButton("⋆ الاوامر", callback_data="cbcmds"),
                       InlineKeyboardButton("⋆ المطور", url=f"https://t.me/{OWNER_NAME}"),
                   ],
                   [
                       InlineKeyboardButton(
                          "⋆ قناة السورس", url=f"https://t.me/{UPDATES_CHANNEL}"
                       ),
                   ],
               ]
             )
           )
        except Exception as error:
           await message.reply_photo(
           photo="https://telegra.ph/file/dd6c46b812395a1b607e9.jpg",
           caption=f"""⋆ **مرحبا {message.from_user.mention()} **\n
⋆ **انا بوت استطيع تشغيل الموسيقي والفديو في محادثتك الصوتية
⋆ **تعلم طريقة تشغيلي واوامر التحكم بي عن طريق  » ⋆ الاوامر !**

⋆ **لتعلم طريقة تشغيلي بمجموعتك اضغط علي » ⋆اوامر اساسيه **
معرف الحساب المساعد @{ASSISTANT_NAME}""",
           reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton("➕ أضفني لمجموعتك ➕",
                           url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                       )
                   ],
                   [InlineKeyboardButton("⋆ الاوامر الاساسيه", callback_data="cbhowtouse")],
                   [
                       InlineKeyboardButton("⋆ الاوامر", callback_data="cbcmds"),
                       InlineKeyboardButton("⋆ المطور", url=f"https://t.me/{OWNER_NAME}"),
                   ],
                   [
                       InlineKeyboardButton(
                          "⋆ قناة السورس", url=f"https://t.me/{UPDATES_CHANNEL}"
                       ),
                   ],
               ]
             )
           )
@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("جاري قياس البينج...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 بينج\n" f"⚡️ `{delta_ping * 1000:.3f} ms`\nكلما كان الرقم اقل كان أفضل")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 حاله البوت:\n"
        f"• **وقت التشغيل:** `{uptime}`\n"
        f"• **وقت البدء:** `{START_TIME_ISO}`"
    )

@Client.on_message(command(["speedtest", f"speedtest@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def speed_test(_, message):
    m = await message.reply_text("قايس سرعة السيرفر\nالحالة : جاري البدء")
    try:
        test = speedtest.Speedtest()
        m = await m.edit("قايس سرعة السيرفر\nالحالة : الاتصال بي سيرفر القياس")
        test.get_best_server()
        m = await m.edit("قايس سرعة السيرفر\nالحالة : قياس سرعة التحميل")
        test.download()
        m = await m.edit("قايس سرعة السيرفر\nالحالة : قياس سرعة الرفع")
        test.upload()
        m = await m.edit("قايس سرعة السيرفر\nالحالة : استخاج النتائج")
        test.results.share()
        m = await m.edit("قايس سرعة السيرفر\nالحالة : حساب النتائج")
        result = test.results.dict()
        m = await m.edit("قايس سرعة السيرفر\nالحالة : التقاط صورة")

        output = f"""**نتائج  قياس سرعة السيرفر**
سرعة التحميل : {result["download"]}
سرعة الرفع : {result["upload"]}
البينج : {result["ping"]}
موقع اختبار السرعة : speedtest.net
----------------------
معلومات سيرفر القياس
الاسم : {result['server']['name']}
الموقع : {result['server']['country']}, {result['server']['cc']}
الهوست : {result['server']['host']}
----------------------
معلومات سيرفر الاتصال
الايبي : {result['client']['ip']}
مقدم الخدمة : {result['client']['isp']}
كود الدولة : {result['client']['country']}
"""
        m = await m.edit("قايس سرعة السيرفر\nالحالة : ارسال النتائج")
        await message.reply_photo(photo=result["share"], caption=output)
        m = await m.edit("قايس سرعة السيرفر\nالحالة : تم ارسال النتائج")
        await m.delete()
    except Exception as e:
        return await m.edit(f"خطأ : {e}")
    
