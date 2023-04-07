from main import bot
from main.modules.schedule import send_anime_schedule
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

time = datetime.now()
def check():
  print(time.hour)
  if time.hour == 9:
    send_anime_schedule()


scheduler = BackgroundScheduler()
scheduler.add_job(check, "interval", seconds=3)

scheduler.start()
bot.run()
