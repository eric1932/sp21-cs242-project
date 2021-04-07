import os
from typing import Optional

from fastapi import FastAPI, Header
from pydantic import BaseModel

from api_message import *
from util.my_mongo import MyMongoInstance

app = FastAPI()
mongo = MyMongoInstance()


class LoginItem(BaseModel):
    username: str
    password: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(item: LoginItem):
    token = mongo.user_login(item.username, item.password)
    if not token:
        return resp_403_password_mismatch
    else:
        return token


@app.get("/logout/{username}")
async def logout(username: str, token: Optional[str] = Header(None), full_logout: Optional[bool] = False):
    if token:
        result = mongo.user_logout(username, token, full_logout)
        if result:
            return resp_200_logout_success
    return resp_401_logout_fail


@app.get("/show/{token}")
async def show_user_with_token(token: str):
    return mongo.token_to_username(token)


@app.get("/sign_in/{name}")
async def sign_in(name: str):
    exist = (name + ".py") in os.listdir("checkin_scripts")
    if not exist:
        return "script not exist"
    else:
        url = [""]
        exec(f"from checkin_scripts.{name} import Workflow", globals())
        exec("url[0] = Workflow().exec()", globals(), locals())
        return url[0]
