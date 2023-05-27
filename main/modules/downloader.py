import os
import requests
import subprocess
import asyncio
import logging
from main.modules.utils import status

logger = logging.getLogger("Downloader")

async def download_anime(m3u8_url, final_path, name):
    m3u8_content = requests.get(m3u8_url).text

    ts_urls = [line.strip() for line in m3u8_content.split('\n') if line.strip().endswith('.ts')]
    await status(f"Downloading {name}", f"{len(ts_urls)} seconds")
    list = []
    for i, ts_url in enumerate(ts_urls):
        logger.info(f"- Downloading {ts_url}... ({i+1}/{len(ts_urls)})")
        ts_url = f"{m3u8_url.rsplit('/', 1)[0]}/{ts_url}"
        ts_content = requests.get(ts_url).content
        with open(f"ts/file_{i}.ts", "wb") as f:
            f.write(ts_content)
            list.append(f"file_{i}.ts")
    
    logger.info("- All files downloaded successfully.")
    await status(f"Downloaded {name}")

    dir_path = "ts"
    ts_files = [f for f in os.listdir(dir_path) if f.endswith(".ts")]

    args = ["ffmpeg", "-i", "concat:" + "|".join([os.path.join(dir_path, f) for f in list]), "-c", "copy", "output.mp4", "-y"]

    logger.info(args)
    subprocess.run(args)
    logger.info("- All files concatenated.")
    
    await status(f"Encoding {name}", "30 Minutes (Approx)")
    logger.info(f"- Compressing {final_path}")
    args = ["ffmpeg", "-i", "output.mp4", "-c:v", "libx265", "-c:a", "copy", "-preset", "veryfast", "compressed.mp4", "-y"]
    subprocess.run(args)
    
    logger.info(f"- Created final file at {final_path}")
    final = final_path.replace(" ", "-")
    args = ["ffmpeg", "-i", "compressed.mp4", "-i", "subtitles/subs.vtt", "-metadata", 'Encoded By=t.me/Anime_Region', "-c", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=eng", "-metadata:s:s:0", 'title=@Anime_Region', "-map", "0:v", "-map", "0:a", "-map", "1:s", final, "-y"]
    subprocess.run(args)

    
    
    
    
    

    


    
    
