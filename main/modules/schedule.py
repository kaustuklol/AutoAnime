import requests
from main import bot
from pyrogram.types import Message
from config import PUBLIC_CHANNEL_ID

def get_scheduled_animes():
    url = 'https://subsplease.org/api/?f=schedule&h=true&tz=IST'
    res = requests.get(url).json()['schedule']

    animes = []
    for i in res:
        x = {}
        x['title'] = i['title']
        x['link'] = "https://subsplease.org/shows/" + i['page']
        x['time'] = i['time']
        x['aired'] = i['aired']
        animes.append(x)

    return animes
    
async def send_anime_schedule():
    animes = get_scheduled_animes()
    text = "<b>📆 Today's Schedule</b> \n\n"
    if animes == []:
        text += "<b>No Anime Airing Today.</b>\n"
    else:
        for i in animes:
                text += '<b>[</b><code>{}</code><b>] - 📌 {}</b>\n\n'.format(
                    i["time"],
                    i["title"]
                )
    text += "\n<b>⏰ Current TimeZone :</b> <code>IST (UTC +5:30)</code>"
    text += "\n\n<b>❗️ Note :</b> This is not when episodes will be uploaded on channel, it's when they will be released by subsplease"
    try:
        msg = await bot.send_photo(PUBLIC_CHANNEL_ID, photo="main/mizuhara.jpg", caption=text)
    except Exception as e:
        print(e)
    return msg
