import os
from pyrogram import filters
from driver.veez import user, bot

@bot.on_message(filters.new_chat_members)
async def auto_join(ay, message):
    bot_id = (await ay.get_me()).id
    if message.new_chat_members[0].id == bot_id:
       if message.chat.username:
           invite = message.chat.username
       else:
           try:
                invite = await ay.export_chat_invite_link(message.chat.id)
           except:
               await ay.send_message(message.chat.id,"قم بي اعطائي الصلاحيات و كتابة الامر ( انضم )")
               return
       try:
            await user.join_chat(invite)
            await user.send_message(message.chat.id,"انضممت هنا لمساعدة البوت في تشغيل الموسيقي")
            await ay.send_message(message.chat.id,f"✅ تم دخول الحساب المساعد بنجاح")
       except:
            await ay.send_message(message.chat.id,"المساعد لم يستطيع الانضمام بشكل تلقائي قم بي اضافته او اعطائي الصلاحيات و كتابة الامر ( انضم )")
            return

@user.on_message(filters.left_chat_member) 
async def auto_leave(ay, message):
    bot_id = (await ay.get_me()).id 
    if message.left_chat_member.id == bot_id: 
        await user.leave_chat(message.chat.id)
