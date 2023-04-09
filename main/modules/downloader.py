import asyncio
import os
import time
from main import bot
import requests
from config import PRIVATE_CHANNEL_ID

import logging
logger = logging.getLogger("Downloader")

# print(anime_link_name)
async def downloader(url, file):
    response = requests.get(url, stream=True)
    path = f"ep/{file}"
    logger.info(f"Downloading {file}")
    bot.send_message(PRIVATE_CHANNEL_ID, f"Downloading {file}")
    with open(path, "wb") as ep:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                ep.write(chunk)

    bot.send_message(PRIVATE_CHANNEL_ID, f"Downloaded {file}")
    return path



   


         
