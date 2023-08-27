from datetime import datetime
from sys import version_info
from time import time
from info import BOT_USERNAME
from config import (
    ALIVE_IMG,
    OWNER_NAME,
    UPDATES_CHANNEL,
    FORCE_SUBSCRIBE_TEXT,
    SUBSCRIBE,
)
from program import __version__
from driver.filters import command2
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("اسبوع", 60 * 60 * 24 * 7),
    ("يوم", 60 * 60 * 24),
    ("ساعة", 60 * 60),
    ("دقيقة", 60),
    ("ثانيا", 1),
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


@Client.on_message(command2(["سورس"]))
async def alive(client: Client, message: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", message.from_user.id)
           if not statusch.status:
              await message.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await message.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    bot_name = (await client.get_me()).first_name
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📣 قناة البوت", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ]
        ]
    )

    alive = f"""**أنا {bot_name}**
✨ أعمل الأن بشكل طبيعي
🍀 مطوري : @{OWNER_NAME}
✨ إصداري: {__version__}
🍀 إصدار البايوجرام: {pyrover}
✨ إصدار البايثون: {__python_version__}
🍀 إصدار المحادثة الصوتيه: {pytover.__version__}
✨ وقت البدء: {uptime}
"""

    await message.reply_photo(
        photo=f"https://t.me/{BOT_USERNAME}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command2(["بينج"]))
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("جاري قياس البينج...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 بينج\n" f"⚡️ `{delta_ping * 1000:.3f} ms`\nكلما كان الرقم اقل كان أفضل")


@Client.on_message(command2(["مدة التشغيل","مده التشغيل","وقت التشغيل"]))
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 حاله البوت:\n"
        f"• **وقت التشغيل:** `{uptime}`\n"
        f"• **وقت البدء:** `{START_TIME_ISO}`"
    )
