from main import bot
from config import PUBLIC_CHANNEL_ID
import logging
logger = logging.getLogger("Utils")  

def trim(text):
    return text.replace(" ", "").lower()

def r_char(text):
    return text.replace(":", "").replace("/", "").replace("!", "").replace("*", "").replace("'", "").replace("-", "").replace("é", "e").replace(",", "").replace(";", "").replace("|", "").replace(".", "").lower()

def purify(text):
    return text.replace("S2", "Season 2").replace("S3", "Season 3").replace("S4", "Season 4").replace("S5", "Season 5").replace("S6", "Season 6").replace("S7", "Season 7").replace("S8", "Season 8").replace("S9", "Season 9").replace("S10", "Season 10").lower()

from AnilistPython import Anilist
anilist = Anilist()

def eng_name(name):
    try:
#         logger.info(anilist.get_anime_info(name)['name_english'])
        return anilist.get_anime(name)['name_english']
    except Exception as e:
        logger.info(e)
        return name
    
import requests

def get_anime_studio(anime_name):
    # Search for anime by name
    url = "https://graphql.anilist.co"
    query = '''
        query ($search: String) {
            Media(search: $search, type: ANIME) {
                studios(isMain: true) {
                    edges {
                        node {
                            name
                        }
                    }
                }
            }
        }
    '''
    variables = {
        'search': anime_name
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    # Get studio name
    studio_name = data["data"]["Media"]["studios"]["edges"][0]["node"]["name"]

    return studio_name

async def status(sts):
    await bot.edit_message_text(
    chat_id=PUBLIC_CHANNEL_ID,
    message_id=1206,
    text=sts
)
    
