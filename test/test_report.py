import unittest
import os.path

from pypcpe2 import report
from pypcpe2 import read_fasta
from pypcpe2 import comsubseq
from pypcpe2 import utility
from pypcpe2.env import env

import test.env

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

        self.saved_temp_path = env().temp_path
        env().temp_path = self.test_output_folder
        self.temp_path = env().temp_path

    def tearDown(self):
        env().temp_path = self.saved_temp_path

    def test_make_report(self):
        output_path = utility.make_temp_path("machine_output.txt")
        human_output_path = utility.make_temp_path("human_output.txt")

        report.make_report(self.fasta_seq_path1, self.fasta_seq_path2,
                           self.cs_result_bin, output_path, human_output_path)

    # def test_make_human_report(self):
        # x_seqinfo = read_fasta.SeqFileInfo(self.x_seqfile)
        # y_seqinfo = read_fasta.SeqFileInfo(self.y_seqfile)

        # seqs = comsubseq.read_comsubseq_file(self.cs_result_bin)

        # human_output_path = utility.make_temp_path("human_output.txt")

        # report.make_human_report(x_seqinfo, y_seqinfo, seqs, human_output_path)

    # def test_make_machine_report(self):
        # x_seqinfo = read_fasta.SeqFileInfo(self.x_seqfile)
        # y_seqinfo = read_fasta.SeqFileInfo(self.y_seqfile)

        # seqs = comsubseq.read_comsubseq_file(self.cs_result_bin)

        # human_output_path = utility.make_temp_path("machine_output.txt")

        # report.make_machine_report(x_seqinfo, y_seqinfo, seqs, human_output_path)
