import unittest
import os
import os.path

from pypcpe2 import utility
from pypcpe2.env import env

import test.env

class TestUtility(unittest.TestCase):
    def test_make_temp_path(self):
        saved_temp_path = env().temp_path
        env().temp_path = test.env.test_output_folder

        temp_path = os.path.abspath(utility.make_temp_path("test.txt"))
        ans_path = os.path.abspath(os.path.join(test.env.test_output_folder,
                                                "test"))
        self.assertTrue(temp_path, ans_path)


        temp_path = "/home/test/test.txt"
        ans_path = os.path.abspath(os.path.join(test.env.test_output_folder,
                                                "test"))
        self.assertTrue(temp_path, ans_path)

        temp_path = "/home/test/test/test.txt.txt"
        ans_path = os.path.abspath(os.path.join(test.env.test_output_folder,
                                                "test.txt"))
        self.assertTrue(temp_path, ans_path)


