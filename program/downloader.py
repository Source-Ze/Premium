# Copyright (C) 2021 By Veez Music-Project

from __future__ import unicode_literals

import asyncio
import math
import os
import time
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import wget
import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from info import BOT_USERNAME as bn
from config import FORCE_SUBSCRIBE_TEXT, UPDATES_CHANNEL, SUBSCRIBE
from driver.decorators import humanbytes
from driver.filters import command, other_filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

ydl_opts = {
    'format': 'best',
    'keepvideo': True,
    'prefer_ffmpeg': False,
    'geo_bypass': True,
    'outtmpl': '%(title)s.%(ext)s',
    'quite': True
}


@Client.on_message(command(["song", f"song@{bn}", "msong", f"msong@{bn}"]) & ~filters.edited)
async def song(client, message):
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
    query = " ".join(message.command[1:])
    m = await message.reply_text("🔎 يتم البحث عن الأغنية ...")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("⋆ لم أجد الأغنية.\n\nرجاء أعطني اسم صحيح .")
        print(str(e))
        return
    await m.edit("📥 يتم تحميل الأغنية...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**🎧 الرافع  @{bn}**"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("📤 يتم رفع الملف...")
        await message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        await m.delete()
    except Exception as e:
        await m.edit("⋆ حدث خطأ انتظر مالك البوت حتي يصلحه")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


@Client.on_message(
    command(["vsong", f"vsong@{bn}", "video", f"video@{bn}"]) & ~filters.edited
)
async def vsong(client, message):
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
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 **يتم التحميل...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **خطأ:** {e}")
    preview = wget.download(thumbnail)
    await msg.edit("📤 **جاري الرفع...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)


@Client.on_message(command(["lyric", f"lyric@{bn}"]))
async def lyrics(client, message):
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
    try:
        if len(message.command) < 2:
            await message.reply_text("» **اعطني اسم المغني والاغنيه ايضا.**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("🔎 **يتم البحث عن الكلمات...**")
        resp = requests.get(
            f"https://api-tede.herokuapp.com/api/lirik?l={query}"
        ).json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("⋆ **لم استطيع ايجادها.**\n\n» **برجاء اعطائي اسم الاغنيه بشكل صحيح.**")
