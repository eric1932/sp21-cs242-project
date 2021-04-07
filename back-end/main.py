"""
The main api server. Manage users and exec tasks periodically.
"""
import os
from typing import Optional

from fastapi import FastAPI, Header
from pydantic import BaseModel

from api_message import resp_401_logout_fail, resp_200_logout_success, resp_403_password_mismatch
from util.my_mongo import MyMongoInstance

app = FastAPI()
mongo = MyMongoInstance()


class LoginItem(BaseModel):
    """
    POST body
    """
    username: str
    password: str


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
    return token if token else resp_403_password_mismatch  # notTODO return types are not same


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
    exist = (name + ".py") in os.listdir("checkin_scripts")
    if not exist:
        return "script not exist"
    url = [""]
    exec(f"from checkin_scripts.{name} import Workflow", globals())
    exec("url[0] = Workflow().exec()", globals(), locals())
    return url[0]
