import os
import requests
import subprocess
import asyncio
import os
import logging
logger = logging.getLogger("Downloader")

async def download_anime(m3u8_url, final):
    if not os.path.exists("subtitles"):
        os.makedirs("subtitles")
    if not os.path.exists("ts"):
        os.makedirs("ts")
    if not os.path.exists("ep"):
        os.makedirs("ep")
    m3u8_content = requests.get(m3u8_url).text

    ts_urls = [line.strip() for line in m3u8_content.split('\n') if line.strip().endswith('.ts')]

    for i, ts_url in enumerate(ts_urls):
        logger.info(f"- Downloading {ts_url}... ({i+1}/{len(ts_urls)})")
        ts_url = f"{m3u8_url.rsplit('/', 1)[0]}/{ts_url}"
        ts_content = requests.get(ts_url).content
        with open(f"ts/file_{i}.ts", "wb") as f:
            f.write(ts_content)
        # print(f"Downloaded {ts_url}.")
    
    logger.info("- All files downloaded successfully.")

#
    # Set the directory containing the TS files
    dir_path = "ts"

    # Get a list of all the TS files in the directory
    ts_files = [f for f in os.listdir(dir_path) if f.endswith(".ts")]

    # Sort the list of files in ascending order
    ts_files.sort()

    # Create a list of arguments for the ffmpeg command
    args = ["ffmpeg", "-i", "concat:" + "|".join([os.path.join(dir_path, f) for f in ts_files]), "-c", "copy", "output.mp4"]

    # Use subprocess to execute the ffmpeg command
    subprocess.run(args)
    logger.info("done")

    command = 'ffmpeg -i output.mp4 -c:v libx265 -c:a copy -preset veryfast compressed.mp4'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        logger.warning(f"- Error: {error.decode('utf-8')}")
    else:
        print(output.decode('utf-8'))
    logger.info("- Compressed output.mp4 into compressed.mp4")

    for ts_file in ts:
        os.remove(f"ts/{ts_file}")
    os.remove("output.mp4")
    logger.info("- Deleted all downloaded ts files and uncompressed output.mp4.")

    logger.info("- Compressed output.mp4 into compressed.mp4")
    
    command = f'ffmpeg -i compressed.mp4 -i subtitles/subs.vtt -metadata encoded_by="t.me/Anime_Region" -c copy -c:s mov_text -metadata:s:s:0 language=eng -metadata:s:s:0 title="@Anime_Region" final.mp4'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        logger.info(f"- Error: {error.decode('utf-8')}")
    else:
        logger.info(output.decode('utf-8'))
    os.remove("compressed.mp4")
    return ("final.mp4")

