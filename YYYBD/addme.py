from driver.filters import command
from info import ASSISTANT_NAME
from pyrogram import filters
from driver.veez import user as USER

@USER.on_message(command(["addme",f"addme@{ASSISTANT_NAME}"]) & ~filters.edited)
async def leave_one(client, message):
    try:
        if message.from_user.username:
            await USER.add_contact(message.from_user.username, message.from_user.first_name)
        else:
            await USER.add_contact(message.from_user.id, message.from_user.first_name)
        await message.reply_text("تم اضافتك الي جهات الاتصال في الحساب المساعد")
    except Exception as e:
        await message.reply_text(f"خطأ : {e}")
