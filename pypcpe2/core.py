def compare_small_seqs(x_seq_path, y_seq_path):
    return []


def sort_comsubseq_files(input_paths):
    return []


def search_max_comsubseq(input_paths):
    return []


def combine_comsubseq_files(input_paths, output_path):
    return None


def compare_seqs(x_seq_path, y_seq_path):
    output_path = "temp"

    seq_paths = compare_small_seqs(x_seq_path, y_seq_path)

    sorted_paths = sort_comsubseq_files(seq_paths)

    max_seq_paths = search_max_comsubseq(max_seq_paths)

    combine_comsubseq_files(max_combseqs_paths, output_path)

    return output_path


