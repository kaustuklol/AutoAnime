import logging

from pyrogram import Client

from config import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("log.txt"),
    ],
)

logger = logging.getLogger()

bot = Client(
    "AutoAnimeBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="main/modules"),
)
