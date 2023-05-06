import requests
import asyncio
from main.modules.utils import trim, r_char
import os
import logging
logging.getLogger("Consumet - ")

async def m3u8_fetcher(anime):
    base = "https://api.consumet.org/anime/zoro/"
    id = ""
    
    try:
        url = f"{base}{r_char(anime['name_romaji'])}"
        r = requests.get(url)
        results = r.json()['results']
    except:
        url = f"{base}{r_char(anime['name_english'])}"
        r = requests.get(url)
        results = r.json()['results']
    logger.info(results)
    for result in results:
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
        return "None"

    url = f"{base}info?id={id}"
    r = requests.get(url)
    try:
        if anime['next_airing_ep']['episode'] == 1:
            results = r.json()['episodes'][int(anime['next_airing_ep']['episode'])]
        else:
            results = r.json()['episodes'][int(anime['next_airing_ep']['episode'])-2]
    except:
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
