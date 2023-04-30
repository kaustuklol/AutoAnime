import os
import requests
import subprocess
import asyncio
import logging

logger = logging.getLogger("Downloader")

async def download_anime(m3u8_url, final_path):
    if not os.path.exists("subtitles"):
        os.makedirs("subtitles")
    if not os.path.exists("ts"):
        os.makedirs("ts")
    if not os.path.exists("ep"):
        os.makedirs("ep")
    
#     m3u8_content = requests.get(m3u8_url).text

#     ts_urls = [line.strip() for line in m3u8_content.split('\n') if line.strip().endswith('.ts')]

#     for i, ts_url in enumerate(ts_urls):
#         logger.info(f"- Downloading {ts_url}... ({i+1}/{len(ts_urls)})")
#         ts_url = f"{m3u8_url.rsplit('/', 1)[0]}/{ts_url}"
#         ts_content = requests.get(ts_url).content
#         with open(f"ts/file_{i}.ts", "wb") as f:
#             f.write(ts_content)
    
#     logger.info("- All files downloaded successfully.")

    dir_path = "ts"
    ts_files = [f for f in os.listdir(dir_path) if f.endswith(".ts")]
    # Sort the list of files in ascending order
    ts_files.sort()
    logger.info(ts_files)
    # Create a list of arguments for the ffmpeg command
    args = ["ffmpeg", "-i", "concat:" + "|".join([os.path.join(dir_path, f) for f in ts_files]), "-c", "copy", "output.mp4", "-y"]
    # Use subprocess to execute the ffmpeg command
    subprocess.run(args)
    logger.info("- All files concatenated.")
    
    args = ["ffmpeg", "-i", "output.mp4", "-vf", "subtitles=subtitles/subs.vtt", "subs.mp4", "-y"]
    subprocess.run(args)
    logger.info(f"- Created final file at {final_path}")
    
    logger.info(f"- Compressing {final_path}")
    args = ["ffmpeg", "-i", "subs.mp4", "-map", "0", "-c:v", "libx265", "-c:a", "copy", "-crf", "28", "-preset", "ultrafast", "final.mp4", "-y"]
    subprocess.run(args)
    
    
    
    

    


    
    
