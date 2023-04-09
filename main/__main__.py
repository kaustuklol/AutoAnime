from main import bot
from main.modules.schedule import send_anime_schedule, get_scheduled_animes
from datetime import datetime
from config import queue, PRIVATE_CHANNEL_ID, PUBLIC_CHANNEL_ID
import asyncio

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
