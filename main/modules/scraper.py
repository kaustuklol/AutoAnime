import feedparser
import asyncio


async def check_anime():
    info = {}
    animes = []
    rss_url = "https://subsplease.org/rss/?r=720"
    feed = feedparser.parse(rss_url)
    for item in feed['entries']:
        if item['title'] == "[SubsPlease] Ousama Ranking - Yuuki no Takarabako - 01 (720p) [22E80453].mkv":
            info['title'] = item['title']
            info['link'] = item['link']
            info['category'] = item['category'].replace("- 720", "")
            animes.append(info)
            return animes

