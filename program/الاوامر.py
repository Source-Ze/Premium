from driver.filters import command2
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import BOT_USERNAME
from config import (
    OWNER_NAME,
    UPDATES_CHANNEL,
)



@Client.on_message(command2(["الاوامر"]))
async def commands(client, message):
            await message.reply_text(
f"""⋆ **انا بوت استطيع تشغيل الموسيقي والفديو في محادثتك الصوتية **
⋆ **تعلم طريقة تشغيلي واوامر التحكم بي عن طريق  » ⋆ الاوامر**
⋆ **لتعلم طريقة تشغيلي بمجموعتك اضغط علي » ⋆اوامر اساسيه **""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ اضفني لمجموعتك ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("⋆ اوامر اساسيه", callback_data="cbhowtouse")],
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
        ),
        disable_web_page_preview=True,
    )
