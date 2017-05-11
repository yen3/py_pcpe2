import unittest
import os
import os.path

import test.env

from pypcpe2 import comsubseq
from pypcpe2 import env


class TestComSubseq(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = os.path.join(test.env.test_data_folder,
                                             "comsubseq")
        self.test_output_folder = os.path.join(test.env.test_output_folder,
                                               "comsubseq")
        if not os.path.isdir(self.test_output_folder):
            os.makedirs(self.test_output_folder)

        self.saved_temp_path = env.setting().temp_path
        env.setting().temp_path = self.test_output_folder
        self.temp_path = env.setting().temp_path

    def tearDown(self):
        env.setting().temp_path = self.saved_temp_path

    def test_read_comsubseq(self):
        path = os.path.join(self.test_data_folder, "comsubseq.bin")

        seqs = comsubseq.read_comsubseq_file(path)
        ans = [comsubseq.ComSubseq(2, 1, 3, 1, 6),
               comsubseq.ComSubseq(1, 1, 2, 0, 6),
               comsubseq.ComSubseq(2, 1, 2, 0, 6),
               comsubseq.ComSubseq(0, 0, 1, 0, 6),
               comsubseq.ComSubseq(1, 0, 1, 0, 6),
               comsubseq.ComSubseq(2, 0, 1, 0, 6)]

        self.assertEqual(seqs, ans)

    def test_read_empty_comsubseq(self):
        path = os.path.join(self.test_data_folder, "empty_comsubseq.bin")

        seqs = comsubseq.read_comsubseq_file(path)
        self.assertEqual(seqs, [])

