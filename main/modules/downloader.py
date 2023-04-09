import asyncio
import os
import time
import logging

logger = logging.getLogger("Downloader")

import os
import requests


# print(anime_link_name)
async def downloader(url, file):
    response = requests.get(url, stream=True)
    path = f"ep/{file}"
    logger.info(f"Downloading {file}")
    print(f"Downloading {file}")
    with open(path, "wb") as ep:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                ep.write(chunk)
    return path



   


         
