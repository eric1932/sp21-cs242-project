"""
MongoDB manager for this project. Connect & manipulate values.
"""
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
    """
    Which DBs are used should be written down here
    """
    USER = "user"
    TOKENTOUSER = "tokenToUser"


@unique
class UserCollectionAttrs(Enum):
    """
    Attrs in DB:User
    """
    USERNAME = "username"
    PASSWORD = "password"
    TOKENS = "tokens"


@unique
class PymongoUpdateActions(Enum):
    """
    pymongo update_one actions
    """
    SET = "$set"
    PUSH = "$push"
    PULL = "$pull"


def read_env():
    """
    Read MongoDB credentials from environment variables
    :return:
    """
    user_ = os.getenv("DB_USER")
    pass_ = os.getenv("DB_PASS")
    host_ = os.getenv("DB_HOST")
    db_name_ = os.getenv("DB_NAME")
    return user_, pass_, host_, db_name_


class MyMongoInstance:
    """
    MongoDB manager for this project. Connect & manipulate values.
    """
    def __init__(self):
        user, password, host, db_name = read_env()
        self._client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{host}/"
                                           f"?retryWrites=true&w=majority")
        self._database: Database = self._client[db_name]
        self._collections: dict[DBCollections, Collection] = {x: self._database[x.value] for x in DBCollections}

        self._set_up_indexes()

    def _set_up_indexes(self):
        self._collections[DBCollections.USER].create_index([
            (UserCollectionAttrs.USERNAME.value, pymongo.ASCENDING)
        ], unique=True)
        self._collections[DBCollections.TOKENTOUSER].create_index([
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
    def get_collection(self, collection: DBCollections):
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
        :return:
        """
        self._collections[DBCollections.USER].insert_one({
            UserCollectionAttrs.USERNAME.value: username,
            UserCollectionAttrs.PASSWORD.value: credential_helper.hash_password(pw_raw),
            UserCollectionAttrs.TOKENS.value: []
        })

    def user_update(self, username: str, new_pw_raw: str):
        """
        Update user's password
        :param username: username
        :param new_pw_raw: password clear text
        :return:
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
            self._collections[DBCollections.TOKENTOUSER].update_one(
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
        query = self._collections[DBCollections.TOKENTOUSER].find_one({"token": token})
        return query["username"] if query else None
