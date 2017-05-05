import unittest
import os.path

import pcpe2_core

from pypcpe2.env import env
from pypcpe2 import core
from pypcpe2 import comsubseq
import test.env


class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = os.path.join(test.env.test_data_folder, "core")
        self.test_output_folder = os.path.join(test.env.test_output_folder,
                                               "core")
        if not os.path.isdir(self.test_output_folder):
            os.makedirs(self.test_output_folder)

        self.saved_temp_path = env().temp_path
        env().temp_path = self.test_output_folder
        self.temp_path = env().temp_path

        self.saved_output_min_len = env().output_min_len
        env().output_min_len = 6

    def tearDown(self):
        env().temp_path = self.saved_temp_path
        env().output_min_len = self.saved_output_min_len

    def test_compare_small_seqs(self):
        seq1_path = os.path.join(self.test_data_folder, "test1_seq.txt")
        seq2_path = os.path.join(self.test_data_folder, "test2_seq.txt")

        cs_paths = core.compare_small_seqs(seq1_path, seq2_path)

        self.assertEqual(len(cs_paths), 1)
        seqs = comsubseq.read_comsubseq_file(cs_paths[0])

        ans_path = os.path.join(self.test_data_folder, "compare_hash_0")
        ans = comsubseq.read_comsubseq_file(ans_path)

        self.assertEqual(seqs, ans)

    def test_sort_comsubseq_files(self):
        cs_paths = [os.path.join(self.test_data_folder, "compare_hash_0")]
        sorted_paths = core.sort_comsubseq_files(cs_paths)

        ans = [comsubseq.ComSubseq(0, 0, 1, 0, 6),
               comsubseq.ComSubseq(1, 0, 1, 0, 6),
               comsubseq.ComSubseq(1, 1, 2, 0, 6),
               comsubseq.ComSubseq(2, 0, 1, 0, 6),
               comsubseq.ComSubseq(2, 1, 2, 0, 6),
               comsubseq.ComSubseq(2, 1, 3, 1, 6)]

        self.assertEqual(len(sorted_paths), 1)
        seqs = comsubseq.read_comsubseq_file(sorted_paths[0])

        self.assertEqual(seqs, ans)

    def test_max_sorted_comsubsq_files(self):
        sorted_paths = [os.path.join(self.test_data_folder,
                                     "sorted_compare_hash_0")]

        max_paths = core.max_sorted_comsubsq_files(sorted_paths)
        self.assertEqual(len(max_paths), 1)
        seqs = comsubseq.read_comsubseq_file(max_paths[0])

        ans = [comsubseq.ComSubseq(0, 0, 1, 0, 6),
               comsubseq.ComSubseq(1, 0, 1, 0, 6),
               comsubseq.ComSubseq(1, 1, 2, 0, 6),
               comsubseq.ComSubseq(2, 0, 1, 0, 6),
               comsubseq.ComSubseq(2, 1, 2, 0, 7)]

        self.assertEqual(seqs, ans)

    def test_compare_seqs(self):
        seq1_path = os.path.join(self.test_data_folder, "test1_seq.txt")
        seq2_path = os.path.join(self.test_data_folder, "test2_seq.txt")
        result_path = os.path.join(self.test_output_folder, "cs_result.bin")

        core.compare_seqs(seq1_path, seq2_path)
        seqs = comsubseq.read_comsubseq_file(result_path)

        ans = [comsubseq.ComSubseq(0, 0, 1, 0, 6),
               comsubseq.ComSubseq(1, 0, 1, 0, 6),
               comsubseq.ComSubseq(1, 1, 2, 0, 6),
               comsubseq.ComSubseq(2, 0, 1, 0, 6),
               comsubseq.ComSubseq(2, 1, 2, 0, 7)]

        self.assertEqual(seqs, ans)

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
