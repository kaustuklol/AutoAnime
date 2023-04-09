from main import bot
from main.modules.schedule import send_anime_schedule, get_scheduled_animes
from datetime import datetime
from config import queue, PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID
import asyncio
from main.modules.anilist import fetch_anime_info
from main.modules.api import anime_url
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main.modules.downloader import downloader
import main.modules.sudo
from main.modules.upload import uploader
from main.modules.thumbnail import gen_thumb, gen_cover

import logging

logger = logging.getLogger("Bot")

async def update_queue(title):
    title = title.replace("'", "").replace(".", "").replace("-", "").replace("!", "").replace("S2", "Season 2").replace("S3", "Season 3").replace("S4", "Season 4")
    queue.add(title)

async def check_condition():
    print(queue)
    while True:
        animes = get_scheduled_animes()
        current = datetime.now()

        if current.hour == 0 or current.hour == 00 and current.minute<2:
            try:
                animes = get_scheduled_animes()
                msg = await send_anime_schedule()  
                await bot.send_message(PRIVATE_CHANNEL_ID, f"queue: {queue}")
                pin = await bot.pin_chat_message(PUBLIC_CHANNEL_ID, message_id=msg.id)
                await bot.delete_messages(PUBLIC_CHANNEL_ID, pin.id)
            except:
                pass

        for anime in animes:
          if anime['aired'] is True:
            update_queue(anime['title'])
            animes.remove(anime)
            
        if len(queue)>0:
            for anime in queue:
                try:
                    # Search for Anime
                    try:
                        logger.info(f"Currently Working on - {anime}")
                        info = fetch_anime_info(anime['title'])
                    except Exception as e:
                        logger.info(f"Anilist Error Cannot find info of anime named {anime} Error: {e}")
                        break
                    
                    # Fetching url of anime techzapi
                    try:
                        logger.info(f"FetchingUrl of {anime}")
                        url = anime_url("UBDVXP", info['title_english'], info['latest_episode']-1)
                    except Exception as e:
                        logger.info(f"Error Cannot fetch url of {anime} Error: {e}")  
                        break
                        
                    # Download file and generate cover
                    try:
                        title = f"{info['title_english']} - {info['latest_episode']} @Anime_Region_Ongoing"
                        path = await downloader(url, title)
                        path = f"ep/{title}.mp4"
                        cover = await gen_cover(path) 
                        
                    except Exception as e:
                        logger.info(f"Error Occured in downloading or creating cover of {info['title_english']} - {e}")
                        break
                        
                    # Generating thumbnail of anime
                    try:        
                        logger.info(f"Generating thumbnail of: {info['title_english']}")
                        thumb = await gen_thumb(info['title_english'], info['studio'], info['genres'], cover)
                    except Exception as e:
                        logger.info(f"thumb err - {e}")
                        break
                    
                    # Uploading
                    try:
                        logger.info(f"Uploading {info['title_english']}"
                        await uploader(path, thumb, title)
                    except Exception as e:
                        logger.info(f"upload err - {e}")
                        break
                    queue.remove(anime['title'])
                except Exception as e:
                    logger.warning(e)
                        
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
