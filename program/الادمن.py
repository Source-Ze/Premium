from cache.admins import admins
from driver.veez import call_py
from pyrogram import Client, filters
from driver.decorators import authorized_users_only
from driver.filters import command2, other_filters
from driver.queues import QUEUE, clear_queue
from driver.utils import skip_current_song, skip_item
from info import BOT_USERNAME
from config import IMG_3, UPDATES_CHANNEL, FORCE_SUBSCRIBE_TEXT, SUBSCRIBE
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 رجوع", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 اغلاق", callback_data="cls")]]
)


@Client.on_message(command2(["تحديث المسؤولين","تحديث قائمة المسؤولين"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
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
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ ** تم تحديث قائمة الادمن **"
    )


@Client.on_message(command2(["تخطي"]) & other_filters)
#@authorized_users_only
async def skip(client, m: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", m.from_user.id)
           if not statusch.status:
              await m.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await m.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• القائمة", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• اغلاق", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ لا يوحد قائمة تشغيل")
        elif op == 1:
            await m.reply("✅ قائمة التشغيل فارغة\nمغادرة الحساب المساعد للمحادثة الصوتية")
        elif op == 2:
            await m.reply("🗑️ قائمة التشغيل فارغة\nمغادرة الحساب المساعد للمحادثة الصوتية")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **تم التخطي للاغنية التالية.**\n\n🏷 **الاسم:** [{op[0]}]({op[1]})\n💭 **المحادثة:** `{chat_id}`\n💡 **الحالة:** `يشتغل`\n🎧 **مطلوب بوسطة:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **تم حذف قائمة التشغيل:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(command2(["انهاء","ايقاف"]) & other_filters)
#@authorized_users_only
async def stop(client, m: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", m.from_user.id)
           if not statusch.status:
              await m.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await m.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ تم ايقاف التشغيل")
        except Exception as e:
            await m.reply(f"🚫 خطأ:\n\n`{e}`")
    else:
        await m.reply("❌ لا اقوم بتشغيل شيئ")


@Client.on_message(command2(["توقف"]) & other_filters)
@authorized_users_only
async def pause(client, m: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", m.from_user.id)
           if not statusch.status:
              await m.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await m.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ تم عمل ايقاف مؤقت."
            )
        except Exception as e:
            await m.reply(f"🚫 خطأ:\n\n`{e}`")
    else:
        await m.reply("❌ لا اقوم بتشغيل اي شيئ")


@Client.on_message(command2(["استئناف","استكمال"]) & other_filters)
@authorized_users_only
async def resume(client, m: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", m.from_user.id)
           if not statusch.status:
              await m.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await m.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ تم استئناف التشغيل."
            )
        except Exception as e:
            await m.reply(f"🚫 خطأ:\n\n`{e}`")
    else:
        await m.reply("❌ لا اقوم بتشغيل شيئ")


@Client.on_message(command2(["كتم المساعد"]) & other_filters)
@authorized_users_only
async def mute(client, m: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", m.from_user.id)
           if not statusch.status:
              await m.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await m.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 تم كتم الحساب المساعد"
            )
        except Exception as e:
            await m.reply(f"🚫 خطأ:\n\n`{e}`")
    else:
        await m.reply("❌ لا اقوم بتشغيل اي شيئ")


@Client.on_message(command2(["الغاء كتم المساعد","فك كتم المساعد"]) & other_filters)
@authorized_users_only
async def unmute(client, m: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", m.from_user.id)
           if not statusch.status:
              await m.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await m.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 تم الغاء كتم الحساب المساعد"
            )
        except Exception as e:
            await m.reply(f"🚫 خطأ:\n\n`{e}`")
    else:
        await m.reply("❌ لا اقوم بتشغيل اي شيئ")


@Client.on_message(command2(["تعيين مستوي الصوت","تغيير مستوي الصوت","تعين مستوي الصوت","تغير مستوي الصوت","وضع مستوي الصوت","ضع مستوي الصوت"]) & other_filters)
@authorized_users_only
async def change_volume(client, m: Message):
    if SUBSCRIBE == "y":
        try:
           statusch = await client.get_chat_member(f"@{UPDATES_CHANNEL}", m.from_user.id)
           if not statusch.status:
              await m.reply_text(
              text=FORCE_SUBSCRIBE_TEXT,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
              return
        except Exception as error:
            await m.reply_text(
            text=FORCE_SUBSCRIBE_TEXT,
            reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton(text="اشترك في قناة البوت", 
                  url=f"https://telegram.me/{UPDATES_CHANNEL}")]]
            )
         )
            return
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ تم تغيير مستوي الصوت الي `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 خطأ:\n\n`{e}`")
    else:
        await m.reply("❌ لا اقوم بتشغيل شيئ")
