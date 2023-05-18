from main import bot
from main.modules.schedule import send_anime_schedule, get_scheduled_animes
from datetime import datetime
from config import queue, PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID, SUDO_USERS
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram import Client, filters
import main.modules.sudo
import os
from AnilistPython import Anilist
import logging
from main.modules.utils import purify, r_char, status
from main.modules.downloader import download_anime
from main.modules.consumet import m3u8_fetcher
from main.modules.upload import upload
animes = []
anilist = Anilist()
logger = logging.getLogger("Bot")
logger.info("Bot Started uwu!")
from config import downloaded
async def main():
    while True:
        animes = await get_scheduled_animes()
        for anime in animes:
            if anime['aired'] is True:
                queue.add(anime['title'])
        for ani in queue:
            try:
                if ani not in downloaded:
                    item = purify(ani)
                    anime = anilist.get_anime(r_char(item))
                    url = await m3u8_fetcher(anime)
                    
                    file = purify(anime['name_english'])
                    path = await download_anime(url, f"{r_char(file)}.mp4", anime['name_english'])
                    await upload(f"{r_char(file)}.mp4", anime)
                    downloaded.add(ani)
            except Exception as e:
                logger.info(f"- General Error -> {e}")
#         for anime in animes:
#             if anime['aired'] is True:
#                 queue.add(anime['title'])
#         for ani in queue:
#             try:
#                 if ani in queue and ani not in downloaded:
#                     item = purify(ani)
#                     anime = anilist.get_anime(r_char(item))
#                     url = await m3u8_fetcher(anime)
#                     if url == "None":
#                         pass

#                     file = purify(anime['name_english'])
#                     path = await download_anime(url, f"{r_char(file)}.mp4", anime['name_english'])

#                     await upload(f"{r_char(file)}.mp4", anime)
#                     downloaded.add(ani)
#                     queue.remove(ani)
#             except Exception as e:
#                 logger.info(f"- Error -> {e}")

        await asyncio.sleep(60) 
                                    
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    pass
       

@bot.on_message(filters.command("refresh") & filters.user(SUDO_USERS))
async def refresh(client, message):
    await message.reply_text("refreshing...")
    animes = await get_scheduled_animes()
    for anime in animes:
        if anime['aired'] is True:
            queue.add(anime['title'])
    await message.reply_text(queue)
    
@bot.on_message(filters.command("remove") & filters.user(SUDO_USERS))
async def remove(client, message):
    anime = message.text.replace("/remove ", "")
    queue.remove(anime)
    await message.reply_text("removing...")
    await message.reply_text(queue)
    
@bot.on_message(filters.command("add") & filters.user(SUDO_USERS))
async def add(client, message):
    anime = message.text.replace("/add ", "")
    queue.add(anime)
    await message.reply_text("adding...")
    await message.reply_text(queue)
    
@bot.on_message(filters.command("force") & filters.user(SUDO_USERS))
async def force(client, message):
    anime = message.text.replace("/force ", "")
    await message.reply_text("Ok")
    try:
        await message.reply_text(f"Searching for (Force){anime}")
        item = purify(anime)
        anime = anilist.get_anime(r_char(item))
        await message.reply_text(f"Fetching Url -> {anime['name_english']}")
        url = await m3u8_fetcher(anime)
        await message.reply_text(f"Url - {url}")
        file = purify(anime['name_english'])
        path = await download_anime(url, f"{r_char(file)}.mp4", anime['name_english'])
        await upload(f"{r_char(file)}.mp4", anime)
        downloaded.add(anime)
    except Exception as e:
        logger.info(f"- Error -> {e}")
        

@bot.on_message(filters.command("test") & filters.user(SUDO_USERS))
async def test(client, message):
    anime = anilist.get_anime("Kubo Wont Let Me Be Invisible")
    await upload(f"compressed.mp4", anime)
    
@bot.on_message(filters.command("anime") & filters.user(SUDO_USERS))
async def test(client, message):
    name =  message.text.replace("/anime ", "")
    await message.reply_text(anilist.get_anime(name))
   
@bot.on_message(filters.command("clrdownload") & filters.user(SUDO_USERS))
async def clrdownload(client, message):
    try:
        for i in downloaded:
            downloaded.remove(i)
            await message.reply_text("Cleared Downloaded..")
    except Exception as e:
        await message.reply_text(e)
        
@bot.on_message(filters.command("getdownloads") & filters.user(SUDO_USERS))
async def d(client, message):
    try:
        await message.reply_text(downloaded)
    except Exception as e:
        await message.reply_text(e)
        
@bot.on_message(filters.command("rd") & filters.user(SUDO_USERS))
async def d(client, message):
    try:
        anime = message.text.replace("/rd ", "")
        downloaded.remove(anime)
        await message.reply_text("removing...")
        await message.reply_text(downloaded)
    except Exception as e:
        await message.reply_text(e)
        
@bot.on_message(filters.command("ad") & filters.user(SUDO_USERS))
async def ad(client, message):
    try:
        anime = message.text.replace("/ad ", "")
        downloaded.add(anime)
        await message.reply_text("addin...")
        await message.reply_text(downloaded)
    except Exception as e:
        await message.reply_text(e)
        
@bot.on_callback_query()
async def handle_callback_query(client, callback_query):
    data = callback_query.data
    await callback_query.answer(
        show_alert=False,
        url=f"https://t.me/IcyHotRobot?start=hEloo"
    )
with bot:
    bot.loop.run_until_complete(main())
