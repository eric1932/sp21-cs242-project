import os
from enum import Enum, unique

import dotenv
import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

import hash_helper

dotenv.load_dotenv()


@unique
class DBCollections(Enum):
    User = "user"


@unique
class UserCollectionAttrs(Enum):
    Username = "username"
    Password = "password"


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

    def get_collection(self, collection: DBCollections):
        return self._database[collection.value]

    def user_query(self, username: str):
        return self._collections[DBCollections.User].find_one({
            UserCollectionAttrs.Username.value: username
        })

    def user_create(self, username: str, pw_raw: str):
        self._collections[DBCollections.User].insert_one({
            UserCollectionAttrs.Username.value: username,
            UserCollectionAttrs.Password.value: hash_helper.hash_password(pw_raw)
        })

    def user_update(self, username: str, new_pw_raw: str):
        self._collections[DBCollections.User].update_one(
            {UserCollectionAttrs.Username.value: username},
            {"$set": {
                UserCollectionAttrs.Password.value: hash_helper.hash_password(new_pw_raw)
            }}
        )

    def user_login(self, username: str, pw_raw: str):
        pass
