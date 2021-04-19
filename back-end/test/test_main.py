import _thread
import unittest
from typing import List

import uvicorn
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
_thread.start_new_thread(lambda: uvicorn.run(app, host="0.0.0.0", port=8000), ())


class MyTestCase(unittest.TestCase):
    def test_main(self):
        response = client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"message": "Hello World"}, response.json())

    def test_login_invalid(self):
        body = {
            "username": "fake",
            "password": "invalid"
        }
        response = client.post("/login", {}, body)
        self.assertEqual(403, response.status_code)

    def test_logout_invalid(self):
        response = client.get("/logout/user", headers={"token": "invalid"})
        self.assertEqual(401, response.status_code)

    def test_sign_in(self):
        response = client.get("/sign_in/dummy_bg_task")
        self.assertEqual("\"success\"", response.text)

    def test_task_list(self):
        resp = client.get("/task", headers={"token": "084b3e7ab8a28c17e990fcf7e0268c10"})
        self.assertTrue(isinstance(resp.json(), list))

    def test_task_list_invalid(self):
        resp = client.get("/task", headers={"token": "invalid"})
        self.assertEqual(404, resp.status_code)

    def test_task_add_remove_dummy(self):
        resp = client.get("/task/add/dummy_bg_task?note=test", headers={"token": "084b3e7ab8a28c17e990fcf7e0268c10"})
        self.assertTrue("task" in resp.json())
        self.assertTrue("apscheduler_id" in resp.json()["task"])
        self.assertEqual("test", resp.json()["task"]["note"])
        task_id: List = resp.json()["task"]["apscheduler_id"]
        resp = client.get(f"/task/remove/{'-'.join(task_id)}", headers={"token": "084b3e7ab8a28c17e990fcf7e0268c10"})
        self.assertEqual({"status": "success"}, resp.json())

    def test_task_add_invalid(self):
        resp = client.get("/task/add/dummy_bg_task?note=test", headers={"token": "invalid"})
        self.assertEqual(404, resp.status_code)

    def test_task_remove_invalid_token(self):
        resp = client.get("/task/remove/invalid", headers={"token": "invalid"})
        self.assertEqual(404, resp.status_code)

    def test_task_remove_invalid_task(self):
        resp = client.get("/task/remove/invalid", headers={"token": "084b3e7ab8a28c17e990fcf7e0268c10"})
        self.assertEqual("fail", resp.json()["status"])


if __name__ == '__main__':
    unittest.main()
