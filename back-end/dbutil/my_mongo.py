import os

import pymongo
import dotenv
from pymongo.database import Database
from pymongo.collection import Collection

from enum import Enum, unique

dotenv.load_dotenv()


@unique
class DBCollections(Enum):
    User = "user"


def read_env():
    user_ = os.getenv("DB_USER")
    pass_ = os.getenv("DB_PASS")
    host_ = os.getenv("DB_HOST")
    db_name_ = os.getenv("DB_NAME")
    return user_, pass_, host_, db_name_


class MongoInstance:
    def __init__(self):
        user, pw, host, db_name = read_env()
        self._client = pymongo.MongoClient(f"mongodb+srv://{user}:{pw}@{host}/"
                                           f"?retryWrites=true&w=majority")
        self._database: Database = self._client[db_name]
        self._collections: dict[DBCollections, Collection] = {x: self._database[x.value] for x in DBCollections}

        self._set_up_indexes()

    def _set_up_indexes(self):
        self._collections[DBCollections.User].create_index([("username", pymongo.ASCENDING)], unique=True)

    # def get_collection(self, collection: DBCollections):
    #     return self._database[collection.value]

    def query_user(self, username: str):
        return self._collections[DBCollections.User].find_one({"username": username})
