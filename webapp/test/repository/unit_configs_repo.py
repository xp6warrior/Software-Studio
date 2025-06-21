import unittest
import os
from webapp.repository.configs_repo import *

class TestConfigsRepo(unittest.TestCase):

    PATH = "/webapp/webapp/test/results/policy.txt"

    def setUp(self):
        with open(self.PATH, "w") as f:
            f.write("TEST POLICY")

    def tearDown(self):
        if os.path.exists(self.PATH):
            os.remove(self.PATH)

    def test_get_policy_success(self):
        result = get_policy()
        self.assertEqual(result, "TEST POLICY")

    def test_get_policy_fail(self):
        os.remove(self.PATH)
        result = get_policy()
        self.assertFalse(result)

    def test_write_policy(self):
        write_policy("NEW TEST POLICY")
        with open(self.PATH, "r") as f:
            result = f.read()
        self.assertEqual(result, "NEW TEST POLICY")

if __name__ == "__main__":
    unittest.main()