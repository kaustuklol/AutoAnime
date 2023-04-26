import asyncio
from datetime import datetime
from pyrogram import Client, filters
from main import bot
from main.modules.schedule import send_anime_schedule
from config import PUBLIC_CHANNEL_ID, PRIVATE_CHANNEL_ID


@bot.on_message(filters.command("schedule"))
async def refresh(client, message):
    await message.reply_text("Sending...")
    
    msg = await send_anime_schedule()  
    pin = await bot.pin_chat_message(PUBLIC_CHANNEL_ID, message_id=msg.id)
    await bot.delete_messages(PUBLIC_CHANNEL_ID, pin.id)
    
@bot.on_message(filters.command("logs"))
async def logs(client, message):
    await message.reply_text("logs...")
    with open("log.txt", "rb") as f:
        await bot.send_document(chat_id=message.chat.id, document=f, filename="log.txt")
