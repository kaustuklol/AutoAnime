from main import bot
from config import PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import logging
logger = logging.getLogger("Uploader")  

async def uploader(file, thumb, title):
    uploaded = 0
    await bot.send_message(PRIVATE_CHANNEL_ID, f"{file} uploading to private channel, Uploaded: {uploaded}")
    async def progress(current, total):
        uploaded = f"{current * 100 / total:.1f}%"
        logger.info(f"Uploaded: {uploaded}")
        await bot.send_message(PRIVATE_CHANNEL_ID, f"{file}, Uploaded: {uploaded}")

    msg = await bot.send_video(PRIVATE_CHANNEL_ID, file, progress=progress)
    id = msg.id

    logger.info(f"{file} uploaded to private channel")

    keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Watch",
                url=f"https://t.me/IcyHotRobot?start={id}"
            )]])

    await bot.send_photo(PUBLIC_CHANNEL_ID, photo=thumb, caption=title, reply_markup=keyboard)

