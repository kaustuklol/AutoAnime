from main import bot
from config import PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
async def uploader(file, thumb, title):

    async def progress(current, total):
        print(f"{current * 100 / total:.1f}%")

    # msg = await bot.send_video(PRIVATE_CHANNEL_ID, file, progress=progress)
    # id = msg.id
    id = 257
    print(f"{file} uploaded to private channel")

    keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Watch",
                url=f"https://t.me/jhb_bot?start={id}"
            )]])

    await bot.send_photo(PUBLIC_CHANNEL_ID, photo=thumb, caption=title, reply_markup=keyboard)

