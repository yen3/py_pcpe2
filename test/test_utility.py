import unittest
import os
import os.path

from pypcpe2 import utility
from pypcpe2.env import env

import test.env

class TestUtility(unittest.TestCase):
    def setUp(self):
        self.saved_temp_path = env().temp_path
        env().temp_path = test.env.test_output_folder
        self.temp_path = env().temp_path

    def tearDown(self):
        env().temp_path = self.saved_temp_path

    def test_make_temp_path(self):
        # test case 1
        temp_path = os.path.abspath(utility.make_temp_path("test.txt"))
        ans_path = os.path.abspath(os.path.join(self.temp_path, "test"))
        self.assertTrue(temp_path, ans_path)

        # test case 2
        temp_path = "/home/test/test.txt"
        ans_path = os.path.abspath(os.path.join(self.temp_path, "test"))
        self.assertTrue(temp_path, ans_path)

        # test case 3
        temp_path = "/home/test/test/test.txt.txt"
        ans_path = os.path.abspath(os.path.join(self.temp_path, "test.txt"))
        self.assertTrue(temp_path, ans_path)
