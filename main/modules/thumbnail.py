import textwrap
from PIL import Image, ImageDraw, ImageFont
import os
import random
import time
import cv2
import asyncio

async def gen_cover(video_path):
    cap = cv2.VideoCapture(video_path)
    start_time = 60  # 1 minute
    end_time = 90  # 1 minute 30 seconds

    # Set the video capture position randomly between the start and end time
    cap.set(
        cv2.CAP_PROP_POS_MSEC,
        random.randint(start_time * 1000, end_time * 1000),
    )

    # Read a frame from the video
    ret, frame = cap.read()

    # Save the frame as an image
    cv2.imwrite("assets/covers/cover.png", frame)
    # Read the original image
    img = cv2.imread("assets/covers/cover.png")

    # Resize the image to 1960 x 1080 px
    img_resized = cv2.resize(img, (1920, 1080))

    cv2.imwrite("assets/covers/cover.png", img_resized)

    # Release the video capture object
    cap.release()

    return "assets/covers/cover.png"

def wrap(text):
    text = text.split(" ")
    n=0
    txt = ""
    for i in text:
        if n==4:
            txt += "\n\n"
        if n==6:
            txt += "...."
            return txt
        txt += f" {i}"
        n += 1

    return txt

async def gen_thumb(anime_name, studio_name, genre_text_list, cover):
    thumbs = os.listdir("assets/thumbs/")
    
    # Load cover and random thumbnail
    background = Image.open(cover)
    thumb = Image.open(f"assets/thumbs/{random.choice(thumbs)}")
    
    # Resize thumbnail
    new_height = 1080
    aspect_ratio = thumb.width / thumb.height
    new_width = int(new_height * aspect_ratio)
    thumb = thumb.resize((new_width, new_height))
    
    # Add thumbnail to cover
    x = 0   # margin of 50 pixels
    background.paste(thumb, (x, 0), thumb)
    
    # Add text on the thumbnail
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("assets/font1.ttf", 83)
    text = wrap(anime_name)
    text_width, text_height = draw.textsize(text, font)
    x = thumb.width - text_width - 50
    y = (background.height - text_height) // 4
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # Add text on the thumbnail
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("assets/font2.ttf", 50)
    text = studio_name
    text_width, text_height = draw.textsize(text, font)
    x = thumb.width - text_width - 150
    y = (background.height - text_height) // 1.7
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    genre_text = ""
    for i in range(len(genre_text_list)):
        if i==3:
            break
        genre_text += f"•{genre_text_list[i]}  "

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("assets/font2.ttf", 43)
    text = genre_text
    text_width, text_height = draw.textsize(text, font)
    x = 1175
    y = (background.height - text_height) // 1.1
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    
    # background.show()
    background.save("assets/thumbnail.png")

    return "assets/thumbnail.png"
