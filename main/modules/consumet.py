import requests
import asyncio
from main.modules.utils import trim, r_char
import os
import logging
logger = logging.getLogger("Consumet - ")
import time

async def m3u8_fetcher(anime):
    base = "https://api.consumet.org/anime/zoro/"
    id = ""
    logger.info(f"Searching for {anime['name_english']}")
    try:
        s = requests.Session()
        url = f"{base}{r_char(anime['name_romaji'])}?t={format(int(time.time()))}"
        r = s.get(url)
        results = r.json()['results']
    except:
        s = requests.Session()
        url = f"{base}{r_char(anime['name_english'])}?t={format(int(time.time()))}"
        r = s.get(url)
        results = r.json()['results']
    #logger.info(results)
    for result in results:
        #logger.info(trim(r_char(result['title'])))
        #logger.info(trim(r_char(anime['name_english'])))
        if trim(r_char(result['title'])) == trim(r_char(anime['name_english'])):
            id = result['id']
            # print(result['url'])
            break
        elif trim(r_char(result['title'])) == trim(r_char(anime['name_romaji'])):
            id = result['id']
            # print(result['url'])
            break
        else:
            id = results[0]['id']
    if id == "":
        print(url)

    url = f"{base}info?id={id}?t={format(int(time.time()))}"
    s = requests.Session()
    r = s.get(url)
    try:
#         logger.info(r.json())
        if anime['next_airing_ep']['episode'] == 1:
            results = r.json()['episodes'][int(anime['next_airing_ep']['episode'])]
        else:
            results = r.json()['episodes'][int(anime['next_airing_ep']['episode'])-2]
    except Exception as e:
        logger.info(f"Episode Not Found error {e}")
        print("Episode Not Aired Or Can't found")
        return "None"
    id = results['id']
    # print(url)
    # print(id)
    
    url = f"{base}watch?episodeId={id}"
    r = requests.get(url)
    # print(url)
    results = r.json()
    if not os.path.exists("subtitles"):
        os.makedirs("subtitles")
        
    for subtitle in results['subtitles']:
        if subtitle['lang'] == "English":
            url = subtitle['url']
            filename = "subs.vtt"
            response = requests.get(url)
            with open(f"subtitles/{filename}", "wb") as f:
                f.write(response.content)

    return results['sources'][1]['url']
