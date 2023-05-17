from main import bot
from config import PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main.modules.thumbnail import gen_thumb, gen_cover
from main.modules.utils import get_anime_studio, status, change_photo_height
import os
import logging
logger = logging.getLogger("Uploader")  

async def upload(f, anime):
#     await status(f"Uploading {anime['name_english']}", "15 sec")
    file = f.replace(" ", "-")
    uploaded = 0
    await bot.send_message(PRIVATE_CHANNEL_ID, f"{anime['name_english']} uploading to private channel")
    async def progress(current, total):
        uploaded = f"{current * 100 / total:.1f}%"
        logger.info(f"Uploaded: {uploaded}")
#         await bot.send_message(PRIVATE_CHANNEL_ID, f"{file}, Uploaded: {uploaded}")
    cover = await gen_cover(file)   
    try:
        studio = f"By {get_anime_studio(anime['name_english'])} Studios"
    except Exception as e:
        logger.info(f"Studio err -> {e}")
        studio = "@Anime_Region_Ongoing"
    thumb = await gen_thumb(anime['name_english'], studio, anime['genres'], cover)
#     thum = change_photo_height(thumb, 320)
    msg = await bot.send_video(PRIVATE_CHANNEL_ID, file, progress=progress, width=1920, height=1080)
    id = msg.id
    
    
    title = f"{anime['name_english']} - {int(anime['next_airing_ep']['episode'])-1}\n@Anime_Region_Ongoing"   


    logger.info(f"{file} uploaded to private channel")

    keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Watch",
                url=f"https://t.me/IcyHotRobot?start={id}"
            )]])

    await bot.send_photo(PUBLIC_CHANNEL_ID, photo=thumb, caption=title, reply_markup=keyboard)
    os.remove(file)
    await status(f"Doing Nothing!")
