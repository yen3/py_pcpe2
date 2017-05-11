#!/usr/bin/env python3

import logging
import sys

from pypcpe2 import read_fasta
from pypcpe2 import core
from pypcpe2 import report
from pypcpe2 import env


def main():
    paths = env.init_env(sys.argv)

    logging.info("Parse the input fasta files")
    x_paths = read_fasta.parse_fasta_file(paths["x_input_path"])
    y_paths = read_fasta.parse_fasta_file(paths["y_input_path"])

    logging.info("Find the maximum common subsequence")
    comsubseq_path = core.compare_seqs(x_paths.seq_path, y_paths.seq_path)

    logging.info("Prepare the report")
    report.make_report(x_paths, y_paths, comsubseq_path,
                       paths["output_path"], paths["output_human_path"])

    logging.info("Exit from the program.")
