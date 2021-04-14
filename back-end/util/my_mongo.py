"""
MongoDB manager for this project. Connect & manipulate values.
"""
import os
from datetime import datetime
from enum import Enum, unique
from typing import List
from typing import Tuple
from typing import Union

import dotenv
import pymongo
from apscheduler.schedulers.base import BaseScheduler
from pymongo.collection import Collection
from pymongo.database import Database

import util.credential_helper as credential_helper
from util.types import Task, TaskID

dotenv.load_dotenv()

_MONGO_CLIENT_INSTANCE = None
_DATABASE = None
_COLLECTIONS = None


@unique
class DBCollections(Enum):
    """
    Which DBs are used should be written down here
    """
    USER = "user"
    TOKEN_TO_USER = "tokenToUser"


@unique
class UserCollectionAttrs(Enum):
    """
    Attrs in DB:User
    """
    USERNAME = "username"
    PASSWORD = "password"
    TOKENS = "tokens"
    TASKS = "tasks"


@unique
class PymongoUpdateActions(Enum):
    """
    pymongo update_one actions
    """
    SET = "$set"
    PUSH = "$push"
    PULL = "$pull"


def read_env() -> Tuple:
    """
    Read MongoDB credentials from environment variables
    :return: user, pass, host, db_name, db_use_srv
    """
    user_ = os.getenv("DB_USER")
    pass_ = os.getenv("DB_PASS")
    host_ = os.getenv("DB_HOST")
    db_name_ = os.getenv("DB_NAME")
    db_use_srv_: bool = (r := os.getenv("DB_SRV")) is not None and r != "0"
    return user_, pass_, host_, db_name_, db_use_srv_


class MyMongoInstance:
    """
    MongoDB manager for this project. Connect & manipulate values.
    """
    def __init__(self, db_name: str = None):
        global _MONGO_CLIENT_INSTANCE
        global _DATABASE
        global _COLLECTIONS
        user, password, host, db_name_env, db_use_srv = read_env()

        if _MONGO_CLIENT_INSTANCE:
            self.client = _MONGO_CLIENT_INSTANCE
            self._database = _DATABASE
            self._collections = _COLLECTIONS
        else:
            if db_use_srv:
                self.client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{host}/"
                                                  f"?retryWrites=true&w=majority")
            else:
                self.client = pymongo.MongoClient(f"mongodb://{user}:{password}@{host}/"
                                                  f"?retryWrites=true&w=majority")
            self._database: Database = self.client[db_name if db_name else db_name_env]
            self._collections: dict[DBCollections, Collection] = {x: self._database[x.value] for x in DBCollections}

            self._set_up_indexes()

            _MONGO_CLIENT_INSTANCE = self.client
            _DATABASE = self._database
            _COLLECTIONS = self._collections

    def _set_up_indexes(self):
        self._collections[DBCollections.USER].create_index([
            (UserCollectionAttrs.USERNAME.value, pymongo.ASCENDING)
        ], unique=True)
        self._collections[DBCollections.TOKEN_TO_USER].create_index([
            ("token", pymongo.ASCENDING)
        ], unique=True)

    def _user_update_one(self, username: str, action: PymongoUpdateActions, content: dict):
        self._collections[DBCollections.USER].update_one(
            {UserCollectionAttrs.USERNAME.value: username},
            {action.value: content}
        )

    def _user_query(self, username: str):
        return self._collections[DBCollections.USER].find_one({
            UserCollectionAttrs.USERNAME.value: username
        })

    # notTODO remove
    def get_collection(self, collection: DBCollections) -> Collection:
        """
        Get a collection from the database. Limit to those defined in DBCollections
        :param collection: DBCollections' item
        :return: the collection object
        """
        return self._database[collection.value]

    def user_create(self, username: str, pw_raw: str):
        """
        Create a user
        :param username: username
        :param pw_raw: password clear text
        """
        self._collections[DBCollections.USER].insert_one({
            UserCollectionAttrs.USERNAME.value: username,
            UserCollectionAttrs.PASSWORD.value: credential_helper.hash_password(pw_raw),
            UserCollectionAttrs.TOKENS.value: [],
            UserCollectionAttrs.TASKS.value: []
        })

    def user_update(self, username: str, new_pw_raw: str):
        """
        Update user's password
        :param username: username
        :param new_pw_raw: password clear text
        """
        self._user_update_one(username, PymongoUpdateActions.SET, {
            UserCollectionAttrs.PASSWORD.value: credential_helper.hash_password(new_pw_raw)
        })
        # logout after password change
        self._user_update_one(username, PymongoUpdateActions.SET, {
            UserCollectionAttrs.TOKENS.value: []
        })

    def user_login(self, username: str, pw_raw: str) -> Union[str, None]:
        """
        Login a user and get a token
        :param username: username
        :param pw_raw: password clear text
        :return: the token or None if invalid credential
        """
        query = self._user_query(username)
        if query and query[UserCollectionAttrs.PASSWORD.value] == credential_helper.hash_password(pw_raw):
            token = credential_helper.generate_token()
            self._user_update_one(username, PymongoUpdateActions.PUSH, {
                UserCollectionAttrs.TOKENS.value: token
            })
            self._collections[DBCollections.TOKEN_TO_USER].update_one(
                {"token": token},
                {"$set": {"username": username}},
                upsert=True
            )
            return token
        return None

    def user_logout(self, username: str, val_token: str, remove_all: bool = False) -> bool:
        """
        Logout a user and invalidate one/all tokens
        :param username: username
        :param val_token: token for validation
        :param remove_all: if set to True, all tokens related to the user will be invalidated
        :return: True if the operation success
        """
        query = self._user_query(username)
        if query and val_token in query[UserCollectionAttrs.TOKENS.value]:
            if remove_all:
                self._user_update_one(username, PymongoUpdateActions.SET, {
                    UserCollectionAttrs.TOKENS.value: []
                })
            else:
                self._user_update_one(username, PymongoUpdateActions.PULL, {
                    UserCollectionAttrs.TOKENS.value: val_token
                })
            return True
        return False

    def token_to_username(self, token: str) -> Union[str, None]:
        """
        Translate a token into a username
        :param token: token
        :return: username
        """
        query = self._collections[DBCollections.TOKEN_TO_USER].find_one({"token": token})
        return query[UserCollectionAttrs.USERNAME.value] if query else None

    def _task_find_index(self, target_task_id: List[str]):
        query = self._user_query(target_task_id[0])
        tasks: List[Task] = query[UserCollectionAttrs.TASKS.value]
        # TODO magic?
        return [x["apscheduler_id"] == target_task_id for x in tasks].index(True)

    def task_list(self, username: str) -> List[Task]:
        """
        Get tasks given a username.
        :param username: username
        :return: list of tasks
        """
        query = self._user_query(username)
        return query[UserCollectionAttrs.TASKS.value]

    def task_add_to_user(self, username: str, task: Task):
        """
        Add a task item for a user
        :param username: username
        :param task: Task item
        """
        self._user_update_one(username, PymongoUpdateActions.PUSH, {
            UserCollectionAttrs.TASKS.value: task
        })

    def task_update_last_success_time(self, target_task_id: Union[TaskID, str]) -> bool:
        """
        Update last_success_time of a Task to current time.
        :param target_task_id: TaskID to find the Task
        :return: True if success
        """
        if isinstance(target_task_id, TaskID):
            target_task_id = list(target_task_id)
        else:
            target_task_id = target_task_id.split('-')

        # First, find index (also if task exists)
        try:
            index = self._task_find_index(target_task_id)
        except ValueError:
            return False

        # Then, update it with current time
        # TODO magic?
        self._collections[DBCollections.USER].update_one(
            {UserCollectionAttrs.USERNAME.value: target_task_id[0]},
            {"$set": {f"tasks.{index}.last_success_time": datetime.now()}}
        )
        return True

    def task_remove_from_user(self, task_id_str: str) -> bool:
        """
        Remove a task from user/tasks
        :param task_id_str: TaskID as str
        :return: True if success
        """
        task_id = task_id_str.split('-')
        try:
            index = self._task_find_index(task_id)
        except ValueError:
            return False
        # remove from user attr
        self._collections[DBCollections.USER].update_one(
            {UserCollectionAttrs.USERNAME.value: task_id[0]},
            {"$unset": {f"tasks.{index}": 1}}
        )
        self._collections[DBCollections.USER].update_one(
            {UserCollectionAttrs.USERNAME.value: task_id[0]},
            {"$pull": {f"tasks": None}}
        )
        return True
