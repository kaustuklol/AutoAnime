import asyncio
from datetime import datetime
from pyrogram import Client, filters
from main import bot
from main.modules.schedule import get_scheduled_animes, send_anime_schedul
from config import PUBLIC_CHANNEL_ID, PRIVATE_CHANNEL_ID, queue


@bot.on_message(filters.command("refresh"))
async def refresh(client, message):
    await message.reply_text("Refreshing...")

    animes = get_scheduled_animes()
    for anime in animes:
        title = anime['title'].replace("'", "").replace("!", "").replace(".", "").replace("-", "").replace("S2", "Season 2").replace("S3", "Season 3").replace("S4", "Season 4")
        queue.add(title)

    msg = await send_anime_schedule()  
    await bot.send_message(PRIVATE_CHANNEL_ID, f"queue: {queue}")
    pin = await bot.pin_chat_message(PUBLIC_CHANNEL_ID, message_id=msg.id)
    await bot.delete_messages(PUBLIC_CHANNEL_ID, pin.id)

@bot.on_message(filters.command("add_queue"))
async def add(client, message):
    try:
        text = message.text.replace("add_queue ", "")
        queue.add(text)
        bot.send_message(PRIVATE_CHANNEL_ID, queue)
    except Exception as e:
        bot.send_message(message.chat.id, e)

@bot.on_message(filters.command("remove_queue"))
async def remove(client, message):
    try:
        text = message.text.replace("remove_queue ", "")
        queue.remove(text)
        bot.send_message(PRIVATE_CHANNEL_ID, queue)
    except Exception as e:
        bot.send_message(message.chat.id, e)
