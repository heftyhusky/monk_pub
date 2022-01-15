import importlib
import sys
from typing import List
from loguru import logger
from db_mission_allocate.tasks.task import upload
from db_mission_allocate.tasks.worker import celeryobj


def Update(user_ids:List[str]):
    for user_id in user_ids:
        logger.info(f"{user_id}")
        # task = upload.s(user_id)
        # task.apply_async()
        task = celeryobj.send_task("upload", args=[user_id])
        task = celeryobj.send_task("calculate", args=[user_id])



if __name__ == "__main__":
    user_ids = sys.argv[1:]
    Update(user_ids)