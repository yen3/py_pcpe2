import unittest
import os
import os.path

import test.env

from pypcpe2 import read_fasta


class TestReadFASTA(unittest.TestCase):
    def test_env(self):
        self.assertTrue(os.path.isdir(test.env.test_data_folder))
        self.assertTrue(os.path.isdir(test.env.test_output_folder))

    def test_retrieve_fasta_id(self):
        id_line1 = ">gi|9999999999|gb|AOS87590|pypcpe2 test sequence1"
        id_line2 = (">gi|1034563939|ref|XP_016858498.1| PREDICTED: "
            "uncharacterized protein LOC102725121 ""isoform X1 [Homo sapiens]")

        self.assertEqual(read_fasta.retrieve_fasta_id(id_line1), '9999999999')
        self.assertEqual(read_fasta.retrieve_fasta_id(id_line2), '1034563939')

    def test_read_fasta_file_seq1(self):
        path = os.path.join(test.env.test_data_folder, 'test_seq1_fasta.txt')

        ans = [('>gi|9999999999|gb|AOS87590|pypcpe2 test sequence1', 'ABCDEFG'),
               ('>gi|9999999998|gb|AOS87590|pypcpe2 test sequence2', 'ABCDEFGH'),
               ('>gi|9999999997|gb|AOS87590|pypcpe2 test sequence3', 'ABCDEFGH'),
               ('>gi|9999999996|gb|AOS87590|pypcpe2 test sequence4', 'ABCDEFGH'),
               ('>gi|9999999995|gb|AOS87590|pypcpe2 test sequence5', 'ABCDEFGHI'),
               ('>gi|9999999994|gb|AOS87590|pypcpe2 test sequence6', 'ABCDEFGHI')]

        fs = [fasta for fasta in read_fasta.read_fasta_file(path)]
        self.assertEqual(ans, fs)

    def test_read_fasta_file_seq2(self):
        path = os.path.join(test.env.test_data_folder, 'test_seq2_fasta.txt')

        ans = [('>gi|9999999993|gb|AOS87590|pypcpe2 test sequence7', 'BCDEFG'),
               ('>gi|9999999992|gb|AOS87590|pypcpe2 test sequence8', 'BCDEFG'),
               ('>gi|9999999991|gb|AOS87590|pypcpe2 test sequence9', 'CDEFGHI'),
               ('>gi|9999999990|gb|AOS87590|pypcpe2 test sequence10', 'CDEFGHI'),
               ('>gi|9999999989|gb|AOS87590|pypcpe2 test sequence11', 'CDEFGHI')]

        fs = [fasta for fasta in read_fasta.read_fasta_file(path)]
        self.assertEqual(ans, fs)

