import unittest
import os.path

from pypcpe2 import report
from pypcpe2 import read_fasta
from pypcpe2 import comsubseq
from pypcpe2 import utility
from pypcpe2 import env

import test.env

def compare_sorted_file_content(x_path, y_path):
    with open(x_path) as fx, open(y_path) as fy:
        xlines = fx.readlines()
        ylines = fy.readlines()

        xlines.sort()
        ylines.sort()
        return xlines == ylines


class TestReport(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = os.path.join(test.env.test_data_folder, "report")
        self.test_output_folder = os.path.join(test.env.test_output_folder,
                                               "report")
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

        self.cs_result_bin = os.path.join(self.test_data_folder,
                                          "cs_result.bin")

        self.saved_temp_path = env.setting().temp_path
        env.setting().temp_path = self.test_output_folder
        self.temp_path = env.setting().temp_path

    def tearDown(self):
        env.setting().temp_path = self.saved_temp_path

    def test_create_record_object(self):
        x_fasta_seq = read_fasta.FastaSeq(self.fasta_seq_path1)
        y_fasta_seq = read_fasta.FastaSeq(self.fasta_seq_path2)

        css = comsubseq.ComSubseq(0, 0, 1, 0, 6)
        record = report.Record(css, x_fasta_seq, y_fasta_seq)

        self.assertEqual(record.raw_seq, "BCDEFG")
        self.assertEqual(record.raw_seq_length, 6)
        self.assertEqual(record.x_loc, css.x_loc)
        self.assertEqual(record.y_loc, css.y_loc)
        self.assertEqual(record.x_fasta_id_infos,
            {'9999999999': '>gi|9999999999|gb|AOS87590|pypcpe2 test sequence1'})
        self.assertEqual(record.y_fasta_id_infos,
            {'9999999993': '>gi|9999999993|gb|AOS87590|pypcpe2 test sequence7',
             '9999999992': '>gi|9999999992|gb|AOS87590|pypcpe2 test sequence8'})

    def test_creater_reporter_object(self):
        reporter = report.Reporter(self.fasta_seq_path1, self.fasta_seq_path2,
                                   self.cs_result_bin)
        records = reporter.records
        self.assertEqual(len(records), 5)

        x_fasta_seq = read_fasta.FastaSeq(self.fasta_seq_path1)
        y_fasta_seq = read_fasta.FastaSeq(self.fasta_seq_path2)

        comsubseqs = comsubseq.read_comsubseq_file(self.cs_result_bin)
        for index, css in enumerate(comsubseqs):
            self.assertEqual(records[index].raw_seq,
                x_fasta_seq.seqs[css.x].raw_seq[css.x_loc:
                                                css.x_loc + css.length])
            self.assertEqual(records[index].raw_seq,
                y_fasta_seq.seqs[css.y].raw_seq[css.y_loc:
                                                css.y_loc + css.length])
            self.assertEqual(records[index].x_loc, css.x_loc)
            self.assertEqual(records[index].y_loc, css.y_loc)
            self.assertEqual(records[index].raw_seq_length, css.length)

            x_fasta_id_infos = {fid: x_fasta_seq.fasta_id_infos[fid]
                                for fid in x_fasta_seq.seqs[css.x].fasta_ids}
            self.assertEqual(records[index].x_fasta_id_infos, x_fasta_id_infos)

            y_fasta_id_infos = {fid: y_fasta_seq.fasta_id_infos[fid]
                                for fid in y_fasta_seq.seqs[css.y].fasta_ids}
            self.assertEqual(records[index].y_fasta_id_infos, y_fasta_id_infos)

    def test_make_report(self):
        ans_output_path = os.path.join(self.test_data_folder,
                                       "machine_output.txt")
        ans_human_output_path = os.path.join(self.test_data_folder,
                                             "human_output.txt")

        output_path = utility.make_temp_path("machine_output.txt")
        human_output_path = utility.make_temp_path("human_output.txt")
        report.make_report(self.fasta_seq_path1, self.fasta_seq_path2,
                           self.cs_result_bin, output_path, human_output_path)

        compare_sorted_file_content(ans_output_path, output_path)
        compare_sorted_file_content(ans_human_output_path, human_output_path)
