import unittest
import util.credential_helper as helper

HASH_TEXT = "test1234"
HASH_RESULT = "937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244"


class MyTestCase(unittest.TestCase):
    def test_hash_password(self):
        self.assertEqual(bytes.fromhex(HASH_RESULT), helper.hash_password(HASH_TEXT))

    def test_generate_token(self):
        self.assertEqual(32, len(helper.generate_token()))


if __name__ == '__main__':
    unittest.main()
