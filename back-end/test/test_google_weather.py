import unittest

from checkin_tasks.google_weather import Workflow


class MyTestCase(unittest.TestCase):
    def test_exec(self):
        result: str = Workflow().exec()
        print(result)
        self.assertTrue(result.startswith("https://www.google.com/images/branding/"))


if __name__ == '__main__':
    unittest.main()
