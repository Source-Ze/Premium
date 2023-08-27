from driver.filters import command2
from driver.veez import user as USER
from driver.decorators import sudo_users_only

@USER.on_message(command2(["عدد جهات المساعد"]))
@sudo_users_only
async def get_contacts_countU(client, message):
    try:
        count = USER.get_contacts_count()
        await message.reply_text(f"عدد الجهات في الحساب المساعد : {count}")
    except Exception as e:
        await message.reply_text(f"خطأ : {e}")

