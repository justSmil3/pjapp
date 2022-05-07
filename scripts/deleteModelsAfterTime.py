from asyncio import as_completed, current_task
import time
import schedule
import pytz

from api.models import *

from django.db.models.functions import Now
import datetime

def run():
    current_time = datetime.datetime.today()
    x = datetime.datetime(2020, 5, 17)
    creation_time = datetime.datetime(
                        current_time.year - 2,
                        current_time.month,
                        current_time.day, current_time.hour, 
                        current_time.minute, current_time.second,
                        current_time.microsecond, 
                        pytz.UTC)
    
    def job():
        Track.objects.all().filter(created__lt=creation_time).delete()
        
    schedule.every().monday.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(100000) 