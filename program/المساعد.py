from driver.filters import command2
from driver.veez import user as USER
from driver.decorators import sudo_users_only
from pyrogram import Client


@Client.on_message(command2(["عدد جهات المساعد"]))
@sudo_users_only
async def get_contacts_countB(client, message):
    try:
        ahmedyad = USER.get_contacts_count()
        await message.reply_text(f"عدد الجهات في الحساب المساعد : {ahmedyad}")
    except Exception as e:
        await message.reply_text(f"خطأ : {e}")
