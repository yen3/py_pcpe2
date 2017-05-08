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

    x = read_fasta.parse_fasta_file(x_seq_path)
    y = read_fasta.parse_fasta_file(y_seq_path)

    comsubseq_path = core.compare_seqs(x.seq_path, y.seq_path)

    report.make_report(x, y, comsubseq_path,
                       output_path, human_output_path)
