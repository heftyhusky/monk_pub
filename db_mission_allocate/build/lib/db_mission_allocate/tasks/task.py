import importlib
import typing
import json
import time

from db_mission_allocate.backend.db import db
from db_mission_allocate.tasks.worker import celeryobj


from InputStrategy import InputStrategyFromLocal
from celery.utils.log import get_task_logger
from celery import current_task, states
from celery.exceptions import Ignore
import traceback

# 註冊 task, 有註冊的 task 才可以變成任務發送給 rabbitmq
@celeryobj.task(name="upload")
def upload(user_id:str):
    inputobj = InputStrategyFromLocal("data.pkl")
    data = inputobj.get()
    # 上傳資料庫
    db.db_upload(user_id, json.dumps(data.workout))

@celeryobj.task(name="calculate")
def calculate(user_id:str):
    print("calculated")


@celeryobj.task(name='hello.task', bind=True)
def hello_world(self, name):
    try:
        if name == 'error':
            k = 1 / 0
        for i in range(60):
            time.sleep(1)
            self.update_state(state='PROGRESS', meta={'done': i, 'total': 60})
        return {"result": "hello {}".format(str(name))}
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise ex