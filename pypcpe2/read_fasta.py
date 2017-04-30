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
    fasta_id_info = property(**fasta_id_info())


SeqInfo = collections.namedtuple('SeqInfo', ['seq', 'ids'])


class SeqFileInfo(object):
    def __init__(self, seq_file):
        self._seq_file = seq_file
        self._seq_info = list()
        self._id_info = dict()

    def get_seq_info(self, index):
        return self._seq_info[index]

    def get_id_info(sel, fasta_id):
        return self._id_info[fasta_id]


def create_seq_file(path):
    sf = SeqFile(path)
    SeqFile.parse_seqfile(sf)

    return sf
