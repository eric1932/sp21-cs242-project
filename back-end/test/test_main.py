import _thread
import unittest

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

    def test_show_user_with_token_invalid(self):
        response = client.get("/show/invalid")
        self.assertEqual("null", response.text)

    def test_sign_in(self):
        response = client.get("/sign_in/google_weather")
        self.assertTrue("google.com/images" in response.text)


if __name__ == '__main__':
    unittest.main()
