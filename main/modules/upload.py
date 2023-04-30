from main import bot
from config import PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from main.modules.thumbnail import gen_thumb, gen_cover
import os
import logging
logger = logging.getLogger("Uploader")  

async def upload(f, anime):
    file = f.replace(" ", "-")
    uploaded = 0
    await bot.send_message(PRIVATE_CHANNEL_ID, f"{anime['name_english']} uploading to private channel")
    async def progress(current, total):
        uploaded = f"{current * 100 / total:.1f}%"
        logger.info(f"Uploaded: {uploaded}")
#         await bot.send_message(PRIVATE_CHANNEL_ID, f"{file}, Uploaded: {uploaded}")

    msg = await bot.send_video(PRIVATE_CHANNEL_ID, file, progress=progress)
    id = msg.id
    cover = await gen_cover(file)   
    thumb = await gen_thumb(anime['name_english'], "@Anime_Region", anime['genres'], cover)
    title = f"{anime['name_english']} Episode: {int(anime['next_airing_ep']['episode'])-1} - @Anime_Region_Ongoing"   


    logger.info(f"{file} uploaded to private channel")

    keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Watch",
                url=f"https://t.me/IcyHotRobot?start={id}"
            )]])

    await bot.send_photo(PUBLIC_CHANNEL_ID, photo=thumb, caption=title, reply_markup=keyboard)
    os.remove(file)
