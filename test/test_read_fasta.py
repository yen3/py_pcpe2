import unittest
import os.path

from pypcpe2.env import env
from pypcpe2 import read_fasta
from pypcpe2 import utility

import test.env


def compare_sorted_file_content(x_path, y_path):
    with open(x_path) as fx, open(y_path) as fy:
        xlines = fx.readlines()
        ylines = fy.readlines()

        xlines.sort()
        ylines.sort()
        return xlines == ylines


class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = os.path.join(test.env.test_data_folder,
                                             "read_fasta")
        self.test_output_folder = os.path.join(test.env.test_output_folder,
                                               "read_fasta")
        if not os.path.isdir(self.test_output_folder):
            os.makedirs(self.test_output_folder)

        self.fasta_seq_path1 = read_fasta.FastaSeqPath(
            os.path.join(self.test_data_folder, "test1.txt"),
            seq_path=os.path.join(self.test_data_folder, "test1_seq.txt"),
            fasta_id_path=os.path.join(self.test_data_folder, "test1_id.txt"),
            fasta_id_info_path=os.path.join(self.test_data_folder,
                                      "test1_id_info.txt"))

        self.fasta_seq_path2 = read_fasta.FastaSeqPath(
            os.path.join(self.test_data_folder, "test2.txt"),
            seq_path=os.path.join(self.test_data_folder, "test2_seq.txt"),
            fasta_id_path=os.path.join(self.test_data_folder, "test2_id.txt"),
            fasta_id_info_path=os.path.join(self.test_data_folder,
                                      "test2_id_info.txt"))

        self.saved_temp_path = env().temp_path
        env().temp_path = self.test_output_folder
        self.temp_path = env().temp_path


    def tearDown(self):
        env().temp_path = self.saved_temp_path

    def test_retrieve_fasta_id(self):
        id_line1 = ">gi|9999999999|gb|AOS87590|pypcpe2 test sequence1"
        id_line2 = (">gi|1034563939|ref|XP_016858498.1| PREDICTED: "
            "uncharacterized protein LOC102725121 ""isoform X1 [Homo sapiens]")

        self.assertEqual(read_fasta.retrieve_fasta_id(id_line1), '9999999999')
        self.assertEqual(read_fasta.retrieve_fasta_id(id_line2), '1034563939')

    def test_read_fasta_file_seq1(self):
        fs = [fasta for fasta in
              read_fasta.read_fasta_file(self.fasta_seq_path1.raw_path)]

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
              read_fasta.read_fasta_file(self.fasta_seq_path2.raw_path)]

        ans = [('>gi|9999999993|gb|AOS87590|pypcpe2 test sequence7', 'BCDEFG'),
               ('>gi|9999999992|gb|AOS87590|pypcpe2 test sequence8', 'BCDEFG'),
               ('>gi|9999999991|gb|AOS87590|pypcpe2 test sequence9', 'CDEFGHI'),
               ('>gi|9999999990|gb|AOS87590|pypcpe2 test sequence10',
                'CDEFGHI'),
               ('>gi|9999999989|gb|AOS87590|pypcpe2 test sequence11',
                'CDEFGHI')]

        self.assertEqual(ans, fs)

    def test_create_fasta_id_info_file_seq1(self):
        fasta_path = self.fasta_seq_path1.raw_path
        ans_path = self.fasta_seq_path1.fasta_id_info_path
        info_path = os.path.join(self.test_data_folder, 'test1_id_info.txt')

        read_fasta.create_fasta_id_info_file(fasta_path, info_path)

        with open(ans_path) as f_ans, open(info_path) as f_info:
            self.assertEqual(f_ans.read(), f_info.read())

    def test_create_fasta_id_info_file_seq2(self):
        fasta_path = self.fasta_seq_path2.raw_path
        ans_path = self.fasta_seq_path2.fasta_id_info_path
        info_path = os.path.join(self.test_data_folder, 'test2_id_info.txt')

        read_fasta.create_fasta_id_info_file(fasta_path, info_path)

        with open(ans_path) as f_ans, open(info_path) as f_info:
            self.assertEqual(f_ans.read(), f_info.read())

    def test_create_seq_id_file_seq1(self):
        fasta_path = self.fasta_seq_path1.raw_path
        ans_seq_path = self.fasta_seq_path1.seq_path
        ans_id_path = self.fasta_seq_path1.fasta_id_path

        seq_path = os.path.join(self.test_output_folder, 'test1_seq.txt')
        id_path = os.path.join(self.test_output_folder, 'test1_id.txt')

        read_fasta.create_seq_fasta_id_file(fasta_path, seq_path, id_path)

        # Compare with answer
        self.assertTrue(compare_sorted_file_content(ans_seq_path, seq_path))
        self.assertTrue(compare_sorted_file_content(ans_id_path, id_path))

    def test_create_seq_id_file_seq2(self):
        fasta_path = self.fasta_seq_path2.raw_path
        ans_seq_path = self.fasta_seq_path2.seq_path
        ans_id_path = self.fasta_seq_path2.fasta_id_path

        seq_path = os.path.join(self.test_output_folder, 'test2_seq.txt')
        id_path = os.path.join(self.test_output_folder, 'test2_id.txt')

        read_fasta.create_seq_fasta_id_file(fasta_path, seq_path, id_path)

        # Compare with answer
        self.assertTrue(compare_sorted_file_content(ans_seq_path, seq_path))
        self.assertTrue(compare_sorted_file_content(ans_id_path, id_path))

    def test_fasta_seq_path_object_create1(self):
        fasta_seq_path = read_fasta.FastaSeqPath(self.fasta_seq_path1.raw_path)

        ans_raw_path = os.path.join(self.test_data_folder, "test1.txt")
        ans_seq_path = os.path.join(self.test_output_folder, "test1_seq.txt")
        ans_fasta_id_path = os.path.join(self.test_output_folder, "test1_id.txt")
        ans_fasta_id_info_path = os.path.join(self.test_output_folder,
                                        "test1_id_info.txt")

        self.assertEqual(fasta_seq_path.raw_path, ans_raw_path)
        self.assertEqual(fasta_seq_path.seq_path, ans_seq_path)
        self.assertEqual(fasta_seq_path.fasta_id_path, ans_fasta_id_path)
        self.assertEqual(fasta_seq_path.fasta_id_info_path,
                         ans_fasta_id_info_path)

    def test_fasta_seq_path_object_create2(self):
        fasta_seq_path = read_fasta.FastaSeqPath(self.fasta_seq_path2.raw_path)

        ans_raw_path = os.path.join(self.test_data_folder, "test2.txt")
        ans_seq_path = os.path.join(self.test_output_folder, "test2_seq.txt")
        ans_fasta_id_path = os.path.join(self.test_output_folder, "test2_id.txt")
        ans_fasta_id_info_path = os.path.join(self.test_output_folder,
                                        "test2_id_info.txt")

        self.assertEqual(fasta_seq_path.raw_path, ans_raw_path)
        self.assertEqual(fasta_seq_path.seq_path, ans_seq_path)
        self.assertEqual(fasta_seq_path.fasta_id_path, ans_fasta_id_path)
        self.assertEqual(fasta_seq_path.fasta_id_info_path,
                         ans_fasta_id_info_path)

    def test_parse_fasta_file1(self):
        fasta_seq_path = read_fasta.parse_fasta_file(
            self.fasta_seq_path1.raw_path)

        self.assertTrue(compare_sorted_file_content(
            self.fasta_seq_path1.seq_path, fasta_seq_path.seq_path))
        self.assertTrue(compare_sorted_file_content(
            self.fasta_seq_path1.fasta_id_path, fasta_seq_path.fasta_id_path))
        self.assertTrue(compare_sorted_file_content(
            self.fasta_seq_path1.fasta_id_info_path,
            fasta_seq_path.fasta_id_info_path))

    def test_parse_fasta_file2(self):
        fasta_seq_path = read_fasta.parse_fasta_file(
            self.fasta_seq_path2.raw_path)

        self.assertTrue(compare_sorted_file_content(
            self.fasta_seq_path2.seq_path, fasta_seq_path.seq_path))
        self.assertTrue(compare_sorted_file_content(
            self.fasta_seq_path2.fasta_id_path, fasta_seq_path.fasta_id_path))
        self.assertTrue(compare_sorted_file_content(
            self.fasta_seq_path2.fasta_id_info_path,
            fasta_seq_path.fasta_id_info_path))

    def test_create_fasta_id_info_object1(self):
        infos = read_fasta.FastaIDInfos.read_file(
            self.fasta_seq_path1.fasta_id_info_path)

        ans = {'9999999999':
               '>gi|9999999999|gb|AOS87590|pypcpe2 test sequence1',
               '9999999998':
               '>gi|9999999998|gb|AOS87590|pypcpe2 test sequence2',
               '9999999997':
               '>gi|9999999997|gb|AOS87590|pypcpe2 test sequence3',
               '9999999996':
               '>gi|9999999996|gb|AOS87590|pypcpe2 test sequence4',
               '9999999995':
               '>gi|9999999995|gb|AOS87590|pypcpe2 test sequence5',
               '9999999994':
               '>gi|9999999994|gb|AOS87590|pypcpe2 test sequence6'}

        self.assertEqual(len(infos), len(ans))
        self.assertEqual(infos, ans)

    def test_create_fasta_id_info_object2(self):
        infos = read_fasta.FastaIDInfos.read_file(
            self.fasta_seq_path2.fasta_id_info_path)

        ans = {'9999999993':
               '>gi|9999999993|gb|AOS87590|pypcpe2 test sequence7',
               '9999999992':
               '>gi|9999999992|gb|AOS87590|pypcpe2 test sequence8',
               '9999999991':
               '>gi|9999999991|gb|AOS87590|pypcpe2 test sequence9',
               '9999999990':
               '>gi|9999999990|gb|AOS87590|pypcpe2 test sequence10',
               '9999999989':
               '>gi|9999999989|gb|AOS87590|pypcpe2 test sequence11'}

        self.assertEqual(len(infos), len(ans))
        self.assertEqual(infos, ans)

    def test_create_fasta_id_info_object_with_fasta_ids_1(self):
        infos = read_fasta.FastaIDInfos.read_file(
            self.fasta_seq_path1.fasta_id_info_path,
            {"9999999999", "9999999995"})

        ans = {'9999999999':
               '>gi|9999999999|gb|AOS87590|pypcpe2 test sequence1',
               '9999999995':
               '>gi|9999999995|gb|AOS87590|pypcpe2 test sequence5'}

        self.assertEqual(len(infos), len(ans))
        self.assertEqual(infos, ans)

    def test_create_fasta_id_info_object_with_fasta_ids_2(self):
        infos = read_fasta.FastaIDInfos.read_file(
            self.fasta_seq_path2.fasta_id_info_path,
            {"9999999993", "9999999989"})

        ans = {'9999999993':
               '>gi|9999999993|gb|AOS87590|pypcpe2 test sequence7',
               '9999999989':
               '>gi|9999999989|gb|AOS87590|pypcpe2 test sequence11'}

        self.assertEqual(len(infos), len(ans))
        self.assertEqual(infos, ans)

    def test_create_seqs_object1(self):
        seqs = read_fasta.Sequences.read_file(
            self.fasta_seq_path1.seq_path, self.fasta_seq_path1.fasta_id_path)

        ans = {0: read_fasta.Sequence(raw_seq='ABCDEFG',
                                      fasta_ids=['9999999999']),
               1: read_fasta.Sequence(raw_seq='ABCDEFGH',
                                      fasta_ids=['9999999998', '9999999997',
                                                 '9999999996']),
               2: read_fasta.Sequence(raw_seq='ABCDEFGHI',
                                      fasta_ids=['9999999995',
                                                 '9999999994'])}

        self.assertEqual(len(seqs), len(ans))
        self.assertEqual(seqs, ans)

    def test_create_seqs_object2(self):
        seqs = read_fasta.Sequences.read_file(
            self.fasta_seq_path2.seq_path, self.fasta_seq_path2.fasta_id_path)

        ans = {0: read_fasta.Sequence(raw_seq='BCDEFG',
                                      fasta_ids=['9999999993',
                                                 '9999999992']),
               1: read_fasta.Sequence(raw_seq='CDEFGHI',
                                      fasta_ids=['9999999991', '9999999990',
                                                 '9999999989'])}

        self.assertEqual(len(seqs), len(ans))
        self.assertEqual(seqs, ans)

    def test_create_seqs_object_with_sequence_ids_1(self):
        seqs = read_fasta.Sequences.read_file(
            self.fasta_seq_path1.seq_path, self.fasta_seq_path1.fasta_id_path,
        {0, 2})

        ans = {0: read_fasta.Sequence(raw_seq='ABCDEFG',
                                      fasta_ids=['9999999999']),
               2: read_fasta.Sequence(raw_seq='ABCDEFGHI',
                                      fasta_ids=['9999999995',
                                                 '9999999994'])}

        self.assertEqual(len(seqs), len(ans))
        self.assertEqual(seqs, ans)

    def test_create_seqs_object_with_sequence_ids_2(self):
        seqs = read_fasta.Sequences.read_file(
            self.fasta_seq_path2.seq_path, self.fasta_seq_path2.fasta_id_path,
            {0})

        ans = {0: read_fasta.Sequence(raw_seq='BCDEFG',
                                      fasta_ids=['9999999993',
                                                 '9999999992'])}

        self.assertEqual(len(seqs), len(ans))
        self.assertEqual(seqs, ans)

    def test_create_fasta_seq_object_1(self):
        seqs_ans = {
               0: read_fasta.Sequence(raw_seq='ABCDEFG',
                                      fasta_ids=['9999999999']),
               1: read_fasta.Sequence(raw_seq='ABCDEFGH',
                                      fasta_ids=['9999999998', '9999999997',
                                                 '9999999996']),
               2: read_fasta.Sequence(raw_seq='ABCDEFGHI',
                                      fasta_ids=['9999999995',
                                                 '9999999994'])}
        fasta_id_infos_ans = {
            '9999999999': '>gi|9999999999|gb|AOS87590|pypcpe2 test sequence1',
            '9999999998': '>gi|9999999998|gb|AOS87590|pypcpe2 test sequence2',
            '9999999997': '>gi|9999999997|gb|AOS87590|pypcpe2 test sequence3',
            '9999999996': '>gi|9999999996|gb|AOS87590|pypcpe2 test sequence4',
            '9999999995': '>gi|9999999995|gb|AOS87590|pypcpe2 test sequence5',
            '9999999994': '>gi|9999999994|gb|AOS87590|pypcpe2 test sequence6'}

        fs = read_fasta.FastaSeq(self.fasta_seq_path1)
        self.assertEqual(fs.seqs, seqs_ans)
        self.assertEqual(fs.fasta_id_infos, fasta_id_infos_ans)

    def test_create_fasta_seq_object_2(self):
        seqs_ans = {
            0: read_fasta.Sequence(raw_seq='BCDEFG',
                                   fasta_ids=['9999999993', '9999999992']),
            1: read_fasta.Sequence(raw_seq='CDEFGHI',
                                   fasta_ids=['9999999991', '9999999990',
                                              '9999999989'])}
        fasta_id_infos_ans = {
            '9999999993': '>gi|9999999993|gb|AOS87590|pypcpe2 test sequence7',
            '9999999992': '>gi|9999999992|gb|AOS87590|pypcpe2 test sequence8',
            '9999999991': '>gi|9999999991|gb|AOS87590|pypcpe2 test sequence9',
            '9999999990': '>gi|9999999990|gb|AOS87590|pypcpe2 test sequence10',
            '9999999989': '>gi|9999999989|gb|AOS87590|pypcpe2 test sequence11'}

        fs = read_fasta.FastaSeq(self.fasta_seq_path2)
        self.assertEqual(fs.seqs, seqs_ans)
        self.assertEqual(fs.fasta_id_infos, fasta_id_infos_ans)
