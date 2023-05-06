import asyncio
from datetime import datetime
from pyrogram import Client, filters
from main import bot
from main.modules.schedule import send_anime_schedule
from config import PUBLIC_CHANNEL_ID, PRIVATE_CHANNEL_ID, SUDO_USERS, queue, downloaded
from AnilistPython import Anilist
anilist = Anilist()


# base = "https://api.consumet.org/anime/zoro/"
# id = ""

@bot.on_message(filters.command("schedule") & filters.user(SUDO_USERS))
async def refresh(client, message):
    await message.reply_text("Sending...")
    
    msg = await send_anime_schedule()  
    pin = await bot.pin_chat_message(PUBLIC_CHANNEL_ID, message_id=msg.id)
    await bot.delete_messages(PUBLIC_CHANNEL_ID, pin.id)
    
@bot.on_message(filters.command("logs") & filters.user(SUDO_USERS))
async def logs(client, message):
#     await message.reply_text("logs...")
    with open("log.txt", "rb") as f:
        await bot.send_document(chat_id=message.chat.id, document=f)
        
@bot.on_message(filters.command("clearlogs") & filters.user(SUDO_USERS))
async def clrlogs(client, message):
    open('log.txt', 'w').close()
    await message.reply_text("Logs Cleared...")    
    
@bot.on_message(filters.command("emptyqueue") & filters.user(SUDO_USERS))
async def emptyqueue(client, message):
    try:
        for i in queue:
            queue.remove(i)
            await message.reply_text("Emptied Queue..")
    except Exception as e:
        await message.reply_text(e)

@bot.on_message(filters.command("clrdownload") & filters.user(SUDO_USERS))
async def clrdownload(client, message):
    try:
        for i in downloaded:
            downloaded.remove(i)
            await message.reply_text("Cleared Downloaded..")
    except Exception as e:
        await message.reply_text(e)
        
@bot.on_message(filters.command("getqueue") & filters.user(SUDO_USERS))
async def getqueue(client, message):
    try:
        await message.reply_text(queue)
    except Exception as e:
        await message.reply_text(e)

@bot.on_message(filters.command("getdownloads") & filters.user(SUDO_USERS))
async def d(client, message):
    try:
        await message.reply_text(downloaded)
    except Exception as e:
        await message.reply_text(e)
        
@bot.on_message(filters.command("rd") & filters.user(SUDO_USERS))
async def d(client, message):
    try:
        anime = message.text.replace("/remove ", "")
        downloaded.remove(anime)
        await message.reply_text("removing...")
        await message.reply_text(downloaded)
    except Exception as e:
        await message.reply_text(e)

# @bot.on_message(filters.command("zoro") & filters.user(SUDO_USERS))
# async def logs(client, message):
#     await message.reply_text("Searching...")
#     name = message.text.replace("/zoro ", "")
#     try:
#         anime = anilist.get_anime(name)
#         try:
#             url = f"{base}{r_char(anime['name_romaji'])}"
#             r = requests.get(url)
#             results = r.json()['results']
#         except:
#             url = f"{base}{r_char(anime['name_english'])}"
#             r = requests.get(url)
#             results = r.json()['results']

#         for result in results:
#             if trim(r_char(result['title'])) == trim(r_char(anime['name_english'])):
#                 id = result['id']
#                 # print(result['url'])
#                 break
#             elif trim(r_char(result['title'])) == trim(r_char(anime['name_romaji'])):
#                 id = result['id']
#                 # print(result['url'])
#                 break
#             else:
#                 id = results[0]['id']

#         if id == "":
#             await message.reply_text(url)
#             return "None"
        
#         url = f"{base}info?id={id}"
#         await bot.send_message(message.chat.id, f"{url} - {id}")
#         await bot.send_message(message.chat.id, f"Episode Page - {url}")
#     except Exception as e:
#         await message.reply_text(e)
