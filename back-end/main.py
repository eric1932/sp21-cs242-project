"""
The main api server. Manage users and exec tasks periodically.
"""
import datetime
import os
from typing import Optional, Union

from fastapi import FastAPI
from fastapi import Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import checkin_misc.periodic_task_scheduler as sched
from api_message import resp_200_logout_success
from api_message import resp_401_logout_fail
from api_message import resp_403_password_mismatch
from api_message import resp_404_invalid_token
from util.my_mongo import MyMongoInstance
from util.types import Task, TaskID, TaskStatus

app = FastAPI()
mongo = MyMongoInstance()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO fastapi_logging

class LoginItem(BaseModel):
    """
    POST body
    """
    username: str
    password: str


@app.on_event("startup")
async def startup_event():  # pragma: no cover
    """
    Actions performed when FastAPI starts up.
    :return:
    """
    sched.api_startup()


@app.on_event("shutdown")
async def shutdown_event():  # pragma: no cover
    """
    Actions performed when FastAPI goes down.
    """
    sched.api_shutdown()


@app.get("/")
async def root():
    """
    Hello world!
    :return:
    """
    return {"message": "Hello World"}


@app.post("/login")
async def login(item: LoginItem):
    """
    Verity user&pass and return a token
    :param item: POST body: username & password
    :return: token or error digest
    """
    token = mongo.user_login(item.username, item.password)
    return {"status": "success", "token": token} if token else resp_403_password_mismatch  # notTODO return types are not same


@app.get("/logout/{username}")
async def logout(username: str, token: Optional[str] = Header(None), full_logout: Optional[bool] = False):
    """
    Invalidate one/all tokens given a valid token
    :param username: user to logout
    :param token: a valid token for verification
    :param full_logout: invalidates all token if set to True
    :return: digest
    """
    if token:
        result = mongo.user_logout(username, token, full_logout)
        if result:
            return resp_200_logout_success
    return resp_401_logout_fail


@app.get("/show/{token}")
async def show_user_with_token(token: str):
    """
    Translate token into username
    :param token: some token
    :return: username
    """
    return mongo.token_to_username(token)


@app.get("/sign_in/{name}")
async def sign_in(name: str):
    """
    Execute sign_in scripts with given name
    :param name: sign_in script name
    :return: some info related to this sign_in
    """
    # todo integrate with scheduler & reschedule job & update last success time
    if os.getcwd().endswith("test"):
        os.chdir("..")
    exist = (name + ".py") in os.listdir("checkin_tasks")
    if not exist:
        return "script not exist"
    url = [""]
    exec(f"from checkin_tasks.{name} import Workflow", globals())  # TODO remove
    exec("url[0] = Workflow().exec()", globals(), locals())
    return url[0]


@app.get("/task")
async def user_show_task(token: Optional[str] = Header(None)):
    username = mongo.token_to_username(token)
    if username:
        # TODO pretty
        return mongo.task_list(username)
    else:
        return resp_404_invalid_token


@app.get("/task/add/{template}")
async def user_add_task(template: str,
                        period: int = 3600 * 24,  # default = 1 day
                        note: str = "",
                        cookies: Union[str, dict] = None,
                        token: Optional[str] = Header(None)):
    # TODO cookies not yet implemented
    username = mongo.token_to_username(token)
    if username:
        iter_num = sched.find_job_available_id(username, template)  # TODO async
        task_id = TaskID(username=username, template=template, num=str(iter_num))

        task: Task = {
            "template": template,
            "period": period,
            "note": note,
            "last_success_time": datetime.datetime.min,  # oldest time
            "created_at": datetime.datetime.now(),
            "apscheduler_id": task_id,
            "status": TaskStatus.FIRST_RUN
        }

        # mongo user info update
        mongo.task_add_to_user(username, task)

        # scheduler adding task
        sched.add_task(period, task_id, cookies)

        return {"status": "success", "task": task}
    else:
        return resp_404_invalid_token


@app.get("/task/remove/{task_id_str}")
async def user_remove_task(task_id_str: str,
                           token: Optional[str] = Header(None)):
    username = mongo.token_to_username(token)
    if username:
        if mongo.task_remove_from_user(task_id_str):
            # remove from scheduler
            sched.SCHEDULER.remove_job(task_id_str)
            return {"status": "success"}
        else:
            return {"status": "fail", "error": "cannot find task"}
    else:
        return resp_404_invalid_token
