from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, APIRouter, Request
from message_scheduler import MessageScheduler
from router import router


scheduler = BackgroundScheduler()
app = FastAPI()


app.include_router(router)


try:
    scheduler.add_job(MessageScheduler().create_schedule, trigger=CronTrigger(hour=15, minute=41, second=00))
    scheduler.add_job(MessageScheduler().process_tasks, trigger=CronTrigger(second="0/10"))
    scheduler.start()
except Exception as e:
    print(f"Произошла ошибка: {e}")
