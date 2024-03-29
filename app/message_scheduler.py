from datetime import datetime, timedelta
from redis import StrictRedis
from dotenv import load_dotenv
import requests
import time
import json
import os

load_dotenv()


class MessageScheduler:
    db_queue_name = os.getenv('DB_QUEUE_NAME')
    redis = StrictRedis(host='nq_redis', port=6379, db=0)

    def process_tasks(self) -> None:
        task_list = self.redis.zrange(self.db_queue_name, 0, -1, withscores=True)

        print(task_list)

        for member, score in task_list:
            task_time = score

            if time.time() >= task_time:
                url = os.getenv('NOTICER_BOT_URL') + '/sendMessage'

                json_data = { 'chatId': os.getenv('CHAT_ID'), 'data': member.decode('utf-8') }

                response = requests.post(url, json=json_data)
                if response.status_code == 200:
                    self.redis.zrem(self.db_queue_name, member)
                else:
                    print(f"Ошибка при выполнении запроса. Код ответа: { response.status_code }")

    def add_tasks_to_queue(self, notice_text: str, notice_timestamp: float) -> None:
        self.redis.zadd(self.db_queue_name, {notice_text: notice_timestamp})

    def getNotices(self) -> dict:
        response = requests.get(os.getenv('NOTICER_API_URL') + '/getNotesForNextDay')

        if response.status_code == 200:
            notices = response.json()

            if notices:
                return notices['data']
        else:
            raise Exception("Ошибка при выполнении запроса. Код ответа: " + str(response.status_code))

    def create_schedule(self) -> None:
        for notice in self.getNotices():
            notice_text = notice['text']
            notice_datetime_str = notice['true_datetime']
            original_datetime = datetime.strptime(notice_datetime_str, '%Y-%m-%dT%H:%M:%S')
            notice_timestamp = datetime.timestamp(original_datetime - timedelta(hours=3))

            self.add_tasks_to_queue(json.dumps({'text': notice_text, 'true_datetime': notice_datetime_str}), notice_timestamp)