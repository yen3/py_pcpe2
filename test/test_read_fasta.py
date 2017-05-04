import unittest
import os
import os.path

import test.env

from pypcpe2 import read_fasta
from pypcpe2.env import env


def compare_sorted_file_content(x_path, y_path):
    with open(x_path) as fx, open(y_path) as fy:
        xlines = fx.readlines()
        ylines = fy.readlines()

        xlines.sort()
        ylines.sort()
        return xlines == ylines


class TestReadFASTA(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = test.env.test_data_folder
        self.test_output_folder = test.env.test_output_folder

        self.seqfile1 = read_fasta.SeqFile(
            os.path.join(self.test_data_folder, "test1.txt"),
            seq_path=os.path.join(self.test_data_folder, "test1_seq.txt"),
            id_path=os.path.join(self.test_data_folder, "test1_id.txt"),
            id_info_path=os.path.join(self.test_data_folder,
                                      "test1_id_info.txt"))

        self.seqfile2 = read_fasta.SeqFile(
            os.path.join(self.test_data_folder, "test2.txt"),
            seq_path=os.path.join(self.test_data_folder, "test2_seq.txt"),
            id_path=os.path.join(self.test_data_folder, "test2_id.txt"),
            id_info_path=os.path.join(self.test_data_folder,
                                      "test2_id_info.txt"))

        self.saved_temp_path = env().temp_path
        env().temp_path = self.test_output_folder
        self.temp_path = env().temp_path

    def tearDown(self):
        env().temp_path = self.saved_temp_path

    def test_env(self):
        self.assertTrue(os.path.isdir(self.test_data_folder))
        self.assertTrue(os.path.isdir(self.test_output_folder))

    def test_seq_file_object_create_seq1(self):
        seqfile = read_fasta.SeqFile(self.seqfile1.fasta_path)
        self.assertEqual(seqfile.fasta_path, self.seqfile1.fasta_path)

        ans_seq_path = os.path.join(self.test_output_folder, "test1_seq.txt")
        ans_id_path = os.path.join(self.test_output_folder, "test1_id.txt")
        ans_id_info_path = os.path.join(self.test_output_folder,
                                        "test1_id_info.txt")

        self.assertEqual(seqfile.seq_path, ans_seq_path)
        self.assertEqual(seqfile.id_path, ans_id_path)
        self.assertEqual(seqfile.id_info_path, ans_id_info_path)

    def test_seq_file_object_create_seq2(self):
        seqfile = read_fasta.SeqFile(self.seqfile2.fasta_path)
        self.assertEqual(seqfile.fasta_path, self.seqfile2.fasta_path)

        ans_seq_path = os.path.join(self.test_output_folder, "test2_seq.txt")
        ans_id_path = os.path.join(self.test_output_folder, "test2_id.txt")
        ans_id_info_path = os.path.join(self.test_output_folder,
                                        "test2_id_info.txt")

        self.assertEqual(seqfile.seq_path, ans_seq_path)
        self.assertEqual(seqfile.id_path, ans_id_path)
        self.assertEqual(seqfile.id_info_path, ans_id_info_path)

    def test_retrieve_fasta_id(self):
        id_line1 = ">gi|9999999999|gb|AOS87590|pypcpe2 test sequence1"
        id_line2 = (">gi|1034563939|ref|XP_016858498.1| PREDICTED: "
            "uncharacterized protein LOC102725121 ""isoform X1 [Homo sapiens]")

        self.assertEqual(read_fasta.retrieve_fasta_id(id_line1), '9999999999')
        self.assertEqual(read_fasta.retrieve_fasta_id(id_line2), '1034563939')

    def test_read_fasta_file_seq1(self):
        fs = [fasta for fasta in
              read_fasta.read_fasta_file(self.seqfile1.fasta_path)]

        ans = [('>gi|9999999999|gb|AOS87590|pypcpe2 test sequence1',
                'ABCDEFG'),
               ('>gi|9999999998|gb|AOS87590|pypcpe2 test sequence2',
                'ABCDEFGH'),
               ('>gi|9999999997|gb|AOS87590|pypcpe2 test sequence3',
                'ABCDEFGH'),
               ('>gi|9999999996|gb|AOS87590|pypcpe2 test sequence4',
                'ABCDEFGH'),
               ('>gi|9999999995|gb|AOS87590|pypcpe2 test sequence5',
                'ABCDEFGHI'),
               ('>gi|9999999994|gb|AOS87590|pypcpe2 test sequence6',
                'ABCDEFGHI')]

        self.assertEqual(ans, fs)

    def test_read_fasta_file_seq2(self):
        fs = [fasta for fasta in
              read_fasta.read_fasta_file(self.seqfile2.fasta_path)]

        ans = [('>gi|9999999993|gb|AOS87590|pypcpe2 test sequence7', 'BCDEFG'),
               ('>gi|9999999992|gb|AOS87590|pypcpe2 test sequence8', 'BCDEFG'),
               ('>gi|9999999991|gb|AOS87590|pypcpe2 test sequence9', 'CDEFGHI'),
               ('>gi|9999999990|gb|AOS87590|pypcpe2 test sequence10',
                'CDEFGHI'),
               ('>gi|9999999989|gb|AOS87590|pypcpe2 test sequence11',
                'CDEFGHI')]

        self.assertEqual(ans, fs)

    def test_create_id_info_file_seq1(self):
        fasta_path = self.seqfile1.fasta_path
        ans_path = self.seqfile1.id_info_path
        info_path = os.path.join(self.test_data_folder, 'test1_id_info.txt')

        read_fasta.create_id_info_file(fasta_path, info_path)

        with open(ans_path) as f_ans, open(info_path) as f_info:
            self.assertEqual(f_ans.read(), f_info.read())

    def test_create_id_info_file_seq2(self):
        fasta_path = self.seqfile2.fasta_path
        ans_path = self.seqfile2.id_info_path
        info_path = os.path.join(self.test_data_folder, 'test2_id_info.txt')

        read_fasta.create_id_info_file(fasta_path, info_path)

        with open(ans_path) as f_ans, open(info_path) as f_info:
            self.assertEqual(f_ans.read(), f_info.read())

    def test_create_seq_id_file_seq1(self):
        fasta_path = self.seqfile1.fasta_path
        ans_seq_path = self.seqfile1.seq_path
        ans_id_path = self.seqfile1.id_path

        seq_path = os.path.join(self.test_output_folder, 'test1_seq.txt')
        id_path = os.path.join(self.test_output_folder, 'test1_id.txt')

        read_fasta.create_seq_id_file(fasta_path, seq_path, id_path)

        # Compare with answer
        self.assertTrue(compare_sorted_file_content(ans_seq_path, seq_path))
        self.assertTrue(compare_sorted_file_content(ans_id_path, id_path))

    def test_create_seq_id_file_seq2(self):
        fasta_path = self.seqfile2.fasta_path
        ans_seq_path = self.seqfile2.seq_path
        ans_id_path = self.seqfile2.id_path

        seq_path = os.path.join(self.test_output_folder, 'test2_seq.txt')
        id_path = os.path.join(self.test_output_folder, 'test2_id.txt')

        read_fasta.create_seq_id_file(fasta_path, seq_path, id_path)

        # Compare with answer
        self.assertTrue(compare_sorted_file_content(ans_seq_path, seq_path))
        self.assertTrue(compare_sorted_file_content(ans_id_path, id_path))
