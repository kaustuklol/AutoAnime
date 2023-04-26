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

async def gen_thumb(anime_name, studio_name, genre_text_list, cover):
    thumbs = os.listdir("assets/thumbs/")
    # Open background and thumb images
    background = Image.open("assets/covers/cover.png")
    thumb = Image.open(f"assets/thumbs/{random.choice(thumbs)}")

    # Resize thumb image to new height
    new_height = 1080
    aspect_ratio = thumb.width / thumb.height
    new_width = int(new_height * aspect_ratio)
    thumb = thumb.resize((new_width, new_height))

    # Create a drawing context for the thumb image
    draw = ImageDraw.Draw(thumb)

    # Load desired font file
    font_path = "assets/font1.ttf"
    font_size = 83
    font = ImageFont.truetype(font_path, font_size)

    # Add text to thumb image with desired font
    # anime_name = "The Misfit Of Demon King Academy"
    # print(len(anime_name.replace(" ", "")))

    # Spacing b/w anime_name and genres
    if len(anime_name) <= 30:
        genre_spacing = 90
    else:
        genre_spacing = -60

    def thumb_text(anime_name):
        import textwrap

        wrapped_string = "\n\n".join(
            textwrap.wrap(anime_name, width=20)
        )

        # Print the result
        return wrapped_string.upper()

    anime_name = thumb_text(anime_name)
    anime_name_size = draw.textsize(anime_name, font=font)
    anime_name_position = (
        thumb.width - anime_name_size[0] - 50,
        300,
    )  # 50-top margin 300-right
    draw.text(
        anime_name_position,
        anime_name,
        font=font,
        fill=(255, 255, 255),
    )

    # font file for the studio name text
    new_font_path = "assets/font2.otf"
    new_font_size = 50
    new_font = ImageFont.truetype(new_font_path, new_font_size)

    # Create a drawing context for the thumb image
    new_draw = ImageDraw.Draw(thumb)

    # Calculate position for studio name
    studio_name = f"\n\n @Anime_Region_Ongoing"
    studio_name_size = new_draw.textsize(studio_name, font=new_font)
    studio_name_position = (
        thumb.width - studio_name_size[0] - 50,
        anime_name_position[1] + anime_name_size[1] + -10,
    )  # replace 20 with desired spacing between the two texts

    # Add new text to thumb image with new font
    new_draw.text(
        studio_name_position,
        studio_name,
        font=new_font,
        fill=(255, 255, 255),
    )  # replace fill color as desired

    # Load desired font file for the genre text
    genre_font_path = "assets/font2.otf"
    genre_font_size = 50  # replace with desired font size
    genre_font = ImageFont.truetype(genre_font_path, genre_font_size)

    # Create a drawing context for the thumb image
    genre_draw = ImageDraw.Draw(thumb)

    # Calculate position for the genre new text
    # genre_text_list = ["Action", "Comedy", "Fantasy"]
    genre_text = "\n\n\n\n"
    for i in range(len(genre_text_list)):
        if i==3:
            break
        genre_text += f"•{genre_text_list[i]}  "

    genre_anime_name_size = genre_draw.textsize(
        genre_text, font=genre_font
    )
    genre_anime_name_position = (
        thumb.width - genre_anime_name_size[0] - 250,
        studio_name_position[1] + studio_name_size[1] + genre_spacing,
    )

    # Add the genre new text to thumb image with the genre new font
    genre_draw.text(
        genre_anime_name_position,
        genre_text,
        font=genre_font,
        fill=(255, 255, 255),
    )  # replace fill color as desired

    # Calculate position for right alignment
    x = (
        background.width - thumb.width
    )  # replace 50 with desired right margin

    # Paste thumb image onto background image at new position
    background.paste(
        thumb, (x, 0), thumb
    )  # replace 50 with desired top margin

    # save resulting image
    # background.show()
    background.save("assets/thumbnail.png")

    return "assets/thumbnail.png"

