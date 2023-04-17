from main import bot
from main.modules.schedule import send_anime_schedule
from datetime import datetime
from config import downloaded, PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram import Client, filters
import main.modules.sudo
from main.modules.upload import uploader
from main.modules.thumbnail import gen_thumb, gen_cover
import os
from main.modules.scraper import check_anime
from AnilistPython import Anilist
from torrentp import TorrentDownloader
import logging

anilist = Anilist()
logger = logging.getLogger("Bot")

async def main():
    animes = await check_anime()
    for anime in animes:
        info = await anilist.get_anime(anime['category'])
        if info['name_english'] not in downloaded:
            try:
                try: 
                    torrent_file = await TorrentDownloader(anime['link'], 'ep/')
                except e:
                    torrent_file = TorrentDownloader(anime['link'], 'ep/')
                    
                if int(info['next_airing_ep']['episode']) > 1:
                    airing_ep = int(info['next_airing_ep']['episode'])-1
                
                path = f"ep/{anime['title']}"    
                title = f"{info['name_english']} - {airing_ep} @Anime_Region_Ongoing"

                cover = await gen_cover(path) 
                logger.info(f"Generating thumbnail of: {info['name_english']}")
                thumb = await gen_thumb(info['name_english'], "Anime_Region", info['genres'], cover)

                logger.info(f"Uploading {info['name_english']}")
                await uploader(path, thumb, title)

                downloaded.add(info['name_english'])
                os.remove(f"ep/{anime['title']}")
            except Exception as e:
                print(f"err - {e}")

async def check_condition():
    while True:
        current = datetime.now()

        if current.hour == 0 or current.hour == 00 and current.minute<2:
            try:
                msg = await send_anime_schedule()  
                await bot.send_message(PRIVATE_CHANNEL_ID, f"queue: {queue}")
                pin = await bot.pin_chat_message(PUBLIC_CHANNEL_ID, message_id=msg.id)
                await bot.delete_messages(PUBLIC_CHANNEL_ID, pin.id)
            except:
                pass
            
        await main()
                        
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
with bot:
    bot.loop.run_until_complete(check_condition())
