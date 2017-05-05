import shutil

from pypcpe2 import utility

import pcpe2_core

def compare_small_seqs(x_seq_path, y_seq_path):
    return pcpe2_core.compare_small_seqs(x_seq_path, y_seq_path)


def sort_comsubseq_files(input_paths):
    return  pcpe2_core.sort_comsubseq_files(input_paths)


def search_max_comsubseq(input_paths):
    return pcpe2_core.max_sorted_comsubsq_files


def combine_comsubseq_files(input_paths, output_path):
	with open(output_path, 'wb') as fout:
		for path in input_paths:
			with open(path, 'rb') as fin:
				shutil.copyfileobj(fin, fout)


def compare_seqs(x_seq_path, y_seq_path):

    seq_paths = compare_small_seqs(x_seq_path, y_seq_path)

    sorted_paths = sort_comsubseq_files(seq_paths)

    max_seq_paths = search_max_comsubseq(max_seq_paths)

    output_path = utility.make_temp_path("cs_result.bin")
    combine_comsubseq_files(max_combseqs_paths, output_path)

    return output_path
