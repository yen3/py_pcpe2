"""
Wrapper for pcpe_core external module.

"""
from pypcpe2 import utility

import pcpe2_core

def compare_small_seqs(x_seq_path, y_seq_path):
    """
    Wrapper for pcpe2_core.compare_small_seqs.

    Users should not call the orignal function directly.
    """
    return pcpe2_core.compare_small_seqs(x_seq_path, y_seq_path)


def sort_comsubseq_files(input_paths):
    """
    Wrapper for pcpe2_core.sort_comsubseq_files.

    Users should not call the orignal function directly.
    """
    return pcpe2_core.sort_comsubseq_files(input_paths)


def max_sorted_comsubsq_files(input_paths):
    """
    Wrapper for pcpe2_core.max_sorted_comsubsq_files.

    Users should not call the orignal function directly.
    """
    return pcpe2_core.max_sorted_comsubsq_files(input_paths)


def compare_seqs(x_seq_path, y_seq_path):
    """
    Find all common subseqences for the two seqeuence files.

    Args:
        x_seq_path (str): The input sequence file
        y_seq_path (str): The compared input sequence file

    Return:
        A string present a path which contains list of ComSubseq
    """
    seq_paths = compare_small_seqs(x_seq_path, y_seq_path)
    sorted_paths = sort_comsubseq_files(seq_paths)
    max_seq_paths = max_sorted_comsubsq_files(sorted_paths)
    output_path = utility.make_temp_path("cs_result.bin")
    utility.merge_file(max_seq_paths, output_path)

    return output_path
