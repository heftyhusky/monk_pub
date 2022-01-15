from fastapi import FastAPI, Body
import mysql.connector
import json
from typing import Optional
from pydantic import BaseModel
from db_mission_allocate.tasks.worker import celeryobj
import api.producer as w

from api.config import (
    MYSQL_DATA_USER,
    MYSQL_DATA_PASSWORD,
    MYSQL_DATA_HOST,
    MYSQL_DATA_DATABASE,
    MYSQL_DATA_PORT,
)

app = FastAPI()

class user_data(BaseModel):
    user_id: str
    description: Optional[str] = None

class index(BaseModel):
    user_id: str
    vo2: Optional[str] = None
    fitness_age: Optional[str] = None

@app.get("/result")
def get_widgets(index:index):
    mydb = mysql.connector.connect(
        host=MYSQL_DATA_HOST,
        user=MYSQL_DATA_USER,
        password=MYSQL_DATA_PASSWORD,
        database=MYSQL_DATA_DATABASE
    )
    cursor = mydb.cursor()

    # sql = "SELECT * FROM heartrate WHERE user_id=%(user_id)s"
    # cursor.execute(sql, {'user_id':user_id})
    sql = "SELECT * FROM heartrate WHERE user_id=%s"
    cursor.execute(sql, (index.user_id,))

    row_headers=[x[0] for x in cursor.description] #this will extract row headers

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()

    return json.dumps(json_data)

@app.get("/test")
def read_root():
    return {"Hello": "World"}

@app.post("/user_id/")
async def create_user(payload: user_data):
    task_name = "upload"
    task = celeryobj.send_task(task_name, args=[payload.user_id])
    return dict(id=task.id, url='localhost:8888/check_task/{}'.format(task.id))

@app.get("/test2")
def create_user2(payload: user_data):
    w.Update([payload.user_id])


@app.get("/check_task/{id}")
def check_task(id: str):
    task = celeryobj.AsyncResult(id)
    if task.state == 'SUCCESS':
        response = {
            'status': task.state,
            'result': task.result,
            'task_id': id
        }
    elif task.state == 'FAILURE':
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode('utf-8'))
        del response['children']
        del response['traceback']
    else:
        response = {
            'status': task.state,
            'result': task.info,
            'task_id': id
        }
    return response

# TODO update user_object

# TODO delete user_object
