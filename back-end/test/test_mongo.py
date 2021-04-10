import unittest

from pymongo.collection import Collection

from util.my_mongo import MyMongoInstance, DBCollections
import secrets
import hashlib

instance = MyMongoInstance("test")
password = "test1234"


class MyTestCase(unittest.TestCase):
    def test_get_collection(self):
        col_user = instance.get_collection(DBCollections.USER)
        self.assertIsInstance(col_user, Collection)

    def test_create_and_update_user(self):
        col_user = instance.get_collection(DBCollections.USER)
        username = secrets.token_hex(4)
        instance.user_create(username, password)
        instance.user_update(username, password)
        self.assertEqual(hashlib.sha256(password.encode()).digest(),
                         col_user.find_one({"username": username})["password"])

    def test_user_login_and_logout(self):
        username = secrets.token_hex(4)
        instance.user_create(username, password)
        token = instance.user_login(username, password)
        self.assertEqual(32, len(token))
        self.assertTrue(instance.user_logout(username, token))

    def test_token_to_username(self):
        username = secrets.token_hex(4)
        instance.user_create(username, password)
        token = instance.user_login(username, password)
        self.assertEqual(username, instance.token_to_username(token))


if __name__ == '__main__':
    unittest.main()
