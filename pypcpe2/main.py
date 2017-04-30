#!/usr/bin/env python3

import os
import os.path

from pypcpe2 import read_fasta
from pypcpe2 import core
from pypcpe2 import report


def main():
    x_seq_path = "./x_test"
    y_seq_path = "./y_test"
    output_path = "./output_test"
    human_output_path = "./output_test_human"

    x_seqfile = read_fasta.create_seq_file(x_seq_path)
    y_seqfile = read_fasta.create_seq_file(y_seq_path)

    seq_result = core.compare_seqs(x_seqfile.seq_path, y_seqfile.seq_path)

    report.make_report(x_seqfile, y_seqfile, seq_result,
                       output_path, human_output_path)
