# from main import bot
# from config import PUBLIC_CHANNEL_ID
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from tzlocal import get_localzone
# import asyncio

# # Initialize the scheduler
# scheduler = AsyncIOScheduler(timezone=get_localzone())

# # Function to send the scheduled message
# async def send_message():
#     message = "This is a scheduled message!"  # Replace with your desired message content
#     await bot.send_message(PUBLIC_CHANNEL_ID, message)

# if __name__ == '__main__':
#     # Schedule the send_message function to run every hour
#     scheduler.add_job(send_message, 'interval', hours=12)

#     # Start the bot and scheduler
#     asyncio.get_event_loop().run_until_complete(asyncio.gather(
#         bot.start(),
#         scheduler.start(),
#     ))
import os
from selenium import webdriver

# Download the latest stable version of Chrome
os.system('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')

# Install Chrome
os.system('sudo dpkg -i google-chrome-stable_current_amd64.deb')
os.system('sudo apt-get update')
os.system('sudo apt-get -y install unzip xvfb libxi6 libgconf-2-4')

# Download the latest version of ChromeDriver and set it up
os.system('wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip')
os.system('unzip chromedriver_linux64.zip')
os.system('sudo mv chromedriver /usr/bin/chromedriver')
os.system('sudo chown root:root /usr/bin/chromedriver')
os.system('sudo chmod +x /usr/bin/chromedriver')

# Test if everything is set up correctly by opening Chrome using Selenium
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
driver.get('https://www.google.com')
print(driver.title)
driver.quit()
