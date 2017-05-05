import unittest
import os.path

import pcpe2_core

from pypcpe2.env import env
from pypcpe2 import core
import test.env


class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = test.env.test_data_folder
        self.test_output_folder = test.env.test_output_folder

        self.saved_temp_path = env().temp_path
        env().temp_path = self.test_output_folder
        self.temp_path = env().temp_path

        pcpe2_core.env_set_temp_path(env().temp_path)

    def tearDown(self):
        env().temp_path = self.saved_temp_path

    def test_compare_small_seqs(self):
        seq1_fn = os.path.join(self.test_data_folder, "test1_seq.txt")
        seq2_fn = os.path.join(self.test_data_folder, "test2_seq.txt")

        cs = core.compare_small_seqs(seq1_fn, seq2_fn)
        self.assertEqual(len(cs), 1)

    def test_env_temp_path(self):
        self.assertEqual(self.temp_path,
                         os.path.abspath(pcpe2_core.env_get_temp_path()))

        pcpe2_core.env_set_temp_path(env().temp_path)
        self.assertEqual(pcpe2_core.env_get_temp_path(), env().temp_path)

    def test_env_min_length(self):
        saved_length = pcpe2_core.env_get_min_output_length()

        set_length = 9
        pcpe2_core.env_set_min_output_length(set_length)
        self.assertEqual(pcpe2_core.env_get_min_output_length(), set_length)

        pcpe2_core.env_set_min_output_length(saved_length)
