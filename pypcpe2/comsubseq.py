import os
import os.path
import struct
import collections

ComSubseq = collections.namedtuple('ComSubseq',
                                   ['x', 'y', 'x_loc', 'y_loc', 'length'])

def read_comsubseq_file(path):
    """
    Read binary file which contents list of ComSubseqs

    Args:
        path (str): the read file

    Return:
        A list of ComSubSeq.
    """
    if os.path.getsize(path) == 0:
        return []

    file_size = os.path.getsize(path)
    read_struct = struct.Struct('IIIII')
    struct_size = read_struct.size

    with open(path, 'rb') as fin:
        binary = fin.read()
        seqs = [ComSubseq._make(read_struct.unpack(binary[b:e])) for b, e in
                zip(range(0, file_size, struct_size),
                    range(struct_size, file_size + struct_size, struct_size))]

    return seqs
