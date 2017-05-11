import unittest
import os
import os.path

from pypcpe2 import utility
# from pypcpe2.env import env
from pypcpe2 import env

import test.env

class TestUtility(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = os.path.join(test.env.test_data_folder, "utility")
        self.test_output_folder = os.path.join(test.env.test_output_folder,
                                               "utility")
        if not os.path.isdir(self.test_output_folder):
            os.makedirs(self.test_output_folder)

        self.saved_temp_path = env.setting().temp_path
        env.setting().temp_path = test.env.test_output_folder
        self.temp_path = env.setting().temp_path

    def tearDown(self):
        env.setting().temp_path = self.saved_temp_path

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

    def test_merge_file(self):
        input_paths = [os.path.join(self.test_data_folder, fn)
                       for fn in ['merge1.txt', 'merge2.txt', 'merge3.txt']]
        output_path = utility.make_temp_path('merged.txt')
        ans_path = os.path.join(self.test_data_folder, 'merged.txt')

        utility.merge_file(input_paths, output_path)

        with open(ans_path) as fans, open(output_path) as fout:
            self.assertEqual(fans.read(), fout.read())
