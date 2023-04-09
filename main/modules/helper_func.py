from main import bot
from datetime import datetime
from schedule import get_scheduled_animes, send_anime_schedule

async def update_queue():
    animes = get_scheduled_animes()
    for anime in animes:
        title = anime['title'].replace("'", "").replace(".", "").replace("-", "").replace("S2", "Season 2").replace("S3", "Season 3").replace("S4", "Season 4")
        queue.add(title)
        
    msg = await send_anime_schedule()  
    await bot.send_message(PRIVATE_CHANNEL_ID, f"queue: {queue}")
    pin = await bot.pin_chat_message(PUBLIC_CHANNEL_ID, message_id=msg.id)
    await bot.delete_messages(PUBLIC_CHANNEL_ID, pin.id)