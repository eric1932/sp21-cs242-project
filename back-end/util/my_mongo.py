import os
from enum import Enum, unique
from typing import Union

import dotenv
import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

import util.credential_helper as credential_helper

dotenv.load_dotenv()


@unique
class DBCollections(Enum):
    User = "user"


@unique
class UserCollectionAttrs(Enum):
    Username = "username"
    Password = "password"
    Tokens = "tokens"


@unique
class PymongoUpdateActions(Enum):
    Set = "$set"
    Push = "$push"
    Pull = "$pull"


def read_env():
    user_ = os.getenv("DB_USER")
    pass_ = os.getenv("DB_PASS")
    host_ = os.getenv("DB_HOST")
    db_name_ = os.getenv("DB_NAME")
    return user_, pass_, host_, db_name_


class MyMongoInstance:
    def __init__(self):
        user, pw, host, db_name = read_env()
        self._client = pymongo.MongoClient(f"mongodb+srv://{user}:{pw}@{host}/"
                                           f"?retryWrites=true&w=majority")
        self._database: Database = self._client[db_name]
        self._collections: dict[DBCollections, Collection] = {x: self._database[x.value] for x in DBCollections}

        self._set_up_indexes()

    def _set_up_indexes(self):
        self._collections[DBCollections.User].create_index([
            (UserCollectionAttrs.Username.value, pymongo.ASCENDING)
        ], unique=True)

    def _user_update_one(self, username: str, action: PymongoUpdateActions, content: dict):
        self._collections[DBCollections.User].update_one(
            {UserCollectionAttrs.Username.value: username},
            {action.value: content}
        )

    def _user_query(self, username: str):
        return self._collections[DBCollections.User].find_one({
            UserCollectionAttrs.Username.value: username
        })

    def get_collection(self, collection: DBCollections):
        return self._database[collection.value]

    def user_create(self, username: str, pw_raw: str):
        self._collections[DBCollections.User].insert_one({
            UserCollectionAttrs.Username.value: username,
            UserCollectionAttrs.Password.value: credential_helper.hash_password(pw_raw),
            UserCollectionAttrs.Tokens.value: []
        })

    def user_update(self, username: str, new_pw_raw: str):
        self._user_update_one(username, PymongoUpdateActions.Set, {
            UserCollectionAttrs.Password.value: credential_helper.hash_password(new_pw_raw)
        })
        # logout after password change
        self._user_update_one(username, PymongoUpdateActions.Set, {
            UserCollectionAttrs.Tokens.value: []
        })

    def user_login(self, username: str, pw_raw: str) -> Union[str, None]:
        query = self._user_query(username)
        if query and query[UserCollectionAttrs.Password.value] == credential_helper.hash_password(pw_raw):
            token = credential_helper.generate_token()
            self._user_update_one(username, PymongoUpdateActions.Push, {
                UserCollectionAttrs.Tokens.value: token
            })
            return token
        else:
            return None

    def user_logout(self, username: str, val_token: str, remove_all: bool = False) -> bool:
        query = self._user_query(username)
        if query and val_token in query[UserCollectionAttrs.Tokens.value]:
            if remove_all:
                self._user_update_one(username, PymongoUpdateActions.Set, {
                    UserCollectionAttrs.Tokens.value: []
                })
            else:
                self._user_update_one(username, PymongoUpdateActions.Pull, {
                    UserCollectionAttrs.Tokens.value: val_token
                })
            return True
        else:
            return False
