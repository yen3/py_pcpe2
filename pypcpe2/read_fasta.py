"""
Read/ Parse Fasta file module

The module supports read fasta file and save to related data structures.
"""
import collections

class SeqFile(object):
    def __init__(self, seq_path):
        self._orignal = ""
        self._seq_path = ""
        self._fasta_id_path = ""
        self._fasta_id_info_path = ""

    @staticmethod
    def parse_seqfile(seqfile):
        pass

    def seq_path():
        doc = "The seq_path property."
        def fget(self):
            return self._seq_path
        return locals()
    seq_path = property(**seq_path())

    def fasta_id_path():
        doc = "The fasta_id_path property."
        def fget(self):
            return self._fasta_id_path
        return locals()
    fasta_id_path = property(**fasta_id_path())

    def fasta_id_info_path():
        doc = "The fasta_id_info property."
        def fget(self):
            return self._fasta_id_info_path
        return locals()
    fasta_id_info = property(**fasta_id_info_path())


SeqInfo = collections.namedtuple('SeqInfo', ['seq', 'ids'])


class SeqFileInfo(object):
    def __init__(self, seq_file):
        self._seq_file = seq_file
        self._seq_info = list()
        self._id_info = dict()

    def get_seq_info(self, index):
        return self._seq_info[index]

    def get_id_info(self, fasta_id):
        return self._id_info[fasta_id]


def retrieve_fasta_id(id_line):
    """
    Parse fasta first line to get the fasta id.

    Return:
        id (str)
    """
    return id_line.split('|')[1]


def read_fasta_file(path):
    """
    Generator function for the path.

    Returns:
        info: the first line of the sequences
        seq: the main body of the sequence
    """
    id_line = ""
    seq = ""

    with open(path, 'r') as fin:
        for line in fin:
            if line.startswith('>'):
                if id_line and seq:
                    # Yield the previous one
                    yield id_line, seq
                id_line = line.strip()
                seq = ""
            else:
                seq += line.strip()

    if id_line and seq:
        yield id_line.strip(), seq.strip()


def create_seq_file(path):
    sf = SeqFile(path)
    SeqFile.parse_seqfile(sf)

    return sf
