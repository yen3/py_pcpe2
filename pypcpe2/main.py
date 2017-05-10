#!/usr/bin/env python3

import os
import os.path
import logging

from pypcpe2 import read_fasta
from pypcpe2 import core
from pypcpe2 import report
from pypcpe2.env import env
from pypcpe2.env import init_logging


def main():
    init_logging(level=logging.DEBUG)

    env().output_min_len = 7

    x_seq_path = "./test/testdata/read_fasta/test1.txt"
    y_seq_path = "./test/testdata/read_fasta/test2.txt"
    output_path = "./output_test.txt"
    human_output_path = "./output_test_human.txt"

    logging.info("Parse the input fasta files")
    x = read_fasta.parse_fasta_file(x_seq_path)
    y = read_fasta.parse_fasta_file(y_seq_path)

    logging.info("Find the maximum common subsequence")
    comsubseq_path = core.compare_seqs(x.seq_path, y.seq_path)

    logging.info("Prepare the report")
    report.make_report(x, y, comsubseq_path,
                       output_path, human_output_path)

    logging.info("Exit from the program.")
