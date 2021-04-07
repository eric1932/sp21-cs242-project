from fastapi import FastAPI
from pydantic import BaseModel

from api_message import *
from util.my_mongo import MyMongoInstance
from typing import Optional

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


@app.get("/logout/{username}/{token}")
async def logout(username: str, token: str, full_logout: Optional[bool] = False):
    result = mongo.user_logout(username, token, full_logout)
    if result:
        return resp_200_logout_success
    else:
        return resp_401_logout_fail
