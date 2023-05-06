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


async def main():
    while True:
        for ani in queue:
            try:
                item = purify(ani)
                anime = anilist.get_anime(r_char(item))
                url = await m3u8_fetcher(anime)
                if url == "None":
                    break

                file = purify(anime['name_english'])
                path = await download_anime(url, f"{r_char(file)}.mp4", anime['name_english'])

                await upload(f"{r_char(file)}.mp4", anime)
                queue.remove(ani)
            except Exception as e:
                logger.info(f"- Error -> {e}")

        await asyncio.sleep(60) 
                                    
@bot.on_message(filters.command("start"))
async def start_command(client, message):
    id = message.text.replace("/start", "")
    if id == "":
        message_text = "Hey there! thanks for starting me ~\n\nI am an automated anime uploader bot working on @Anime_Region_Ongoing\n\nJoin our other channels to connect with our community!"
        anime_button = InlineKeyboardButton("Anime", url="https://t.me/Anime_Region")
        group_button = InlineKeyboardButton("Group", url="https://t.me/Anime_Discussion_Region")
        ongoing_anime_button = InlineKeyboardButton("Ongoing Animes", url="https://t.me/Anime_Region_Ongoing")

        btns = InlineKeyboardMarkup([[anime_button, group_button], [ongoing_anime_button]])
        await bot.send_photo(message.chat.id, photo="main/start.jpg", caption=message_text, reply_markup=btns)
    else:
        try:
            id = int(id.replace(" ", ""))
            from main.modules.force_sub import handle_force_subscribe
            fsub = await handle_force_subscribe(bot, message)
            if fsub == 400:
                return
            else:
                await bot.copy_message(message.chat.id, PRIVATE_CHANNEL_ID, id)
                                    
            await bot.copy_message(message.chat.id, PRIVATE_CHANNEL_ID, id)
        except:
            message_text = "Hey there! thanks for starting me ~\n\nI am an automated anime uploader bot working on @Anime_Region_Ongoing\n\nJoin our other channels to connect with our community!"
            anime_button = InlineKeyboardButton("Anime", url="https://t.me/Anime_Region")
            group_button = InlineKeyboardButton("Group", url="https://t.me/Anime_Discussion_Region")
            ongoing_anime_button = InlineKeyboardButton("Ongoing Animes", url="https://t.me/Anime_Region_Ongoing")

            btns = InlineKeyboardMarkup([[anime_button, group_button], [ongoing_anime_button]])
            await bot.send_photo(message.chat.id, photo="main/start.jpg", caption=message_text, reply_markup=btns)
       

@bot.on_message(filters.command("refresh") & filters.user(SUDO_USERS))
async def refresh(client, message):
    await message.reply_text("refreshing...")
    animes = await get_scheduled_animes()
    for anime in animes:
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
    anime = message.text.replace("/force", "")
    await message.reply_text("Ok")
    try:
        logger.info(f"- Searching for (Force){anime}")
        item = purify(anime)
        anime = anilist.get_anime(r_char(item))
        logger.info(f"- Fetching Url -> {anime['name_english']}")
        url = await m3u8_fetcher(anime)
        logger.info(url)
        file = purify(anime['name_english'])
        path = await download_anime(url, f"{r_char(file)}.mp4", anime['name_english'])
#                 await upload(path, anime)
        await upload(f"{r_char(file)}.mp4", anime)
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
    

with bot:
    bot.loop.run_until_complete(main())
