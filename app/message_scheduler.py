from datetime import datetime, timedelta
from redis import StrictRedis
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()


class MessageScheduler:
    db_name = os.getenv('DB_NAME')
    redis = StrictRedis(host='nq_redis', port=6379, db=0)

    def process_tasks(self) -> None:
        task_list = self.redis.zrange(self.db_name, 0, -1, withscores=True)
        for member, score in task_list:
            task_time = score

            if time.time() >= task_time:
                url = os.getenv('NOTICER_BOT_URL') + '/send-message'

                json_data = { 'chatId': os.getenv('CHAT_ID'), 'message': member.decode('utf-8') }

                response = requests.post(url, json=json_data)
                if response.status_code == 200:
                    self.redis.zrem(self.db_name, member)
                else:
                    print(f"Ошибка при выполнении запроса. Код ответа: { response.status_code }")

    def add_tasks_to_queue(self, notice_text: str, notice_timestamp: float) -> None:
        self.redis.zadd(self.db_name, { notice_text: notice_timestamp })

    def getNotices(self) -> dict:
        response = requests.get(os.getenv('NOTICER_API_URL') + '/getAllNotices')

        if response.status_code == 200:
            notices = response.json()

            if notices:
                return notices['data']
        else:
            raise Exception("Ошибка при выполнении запроса. Код ответа: {response.status_code}")

    def create_schedule(self) -> None:
        for notice in self.getNotices():
            notice_text = notice['text']
            notice_datetime = notice['datetime']
            original_datetime = datetime.strptime(notice_datetime, '%d.%m.%Y %H:%M')
            notice_timestamp = datetime.timestamp(original_datetime - timedelta(hours=3))

            self.add_tasks_to_queue(notice_text, notice_timestamp)