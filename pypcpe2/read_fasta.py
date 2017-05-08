"""
Parsing fasta file module.
"""
import os.path
import collections

from pypcpe2 import utility


def retrieve_fasta_id(id_line):
    """
    Parse fasta first line to get the fasta id.

    Return:
        id (str)
    """
    return id_line.split('|')[1]


def read_fasta_file(path):
    """
    Generator function for reading fasta file.

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
        # Yield the last one
        yield id_line.strip(), seq.strip()


def create_seq_fasta_id_file(fasta_path, seq_path, id_path):
    """
    Parse fasta file to make a unique sequence file and a id mapping file.

    The seq file format is as the following

        [number of seqs]
        [len_0] [seq_0]
        [len_1] [seq_1]
        ...
        [len_n] [seq_n]

    The id file format is as the following

        [number of seqs]
        [size_m0] [id_0_0] [id_0_1] ... [id_0_m0]
        [size_m1] [id_1_0] [id_1_1] ... [id_1_m1]
        ...
        [size_mn] [id_n_0] [id_n_1] ... [id_n_mn]

    The seq file and id file is line-to-line mapping. It means the seq has
    one or several fasta ids in the same line number of id file.

    Args:
        fasta_path (str): The input fasta file
        seq_path (str): The output seqeunce file.
        id_path (str): The output id mapping file.
    """
    seq_ids = dict()

    for info, seq in read_fasta_file(fasta_path):
        fasta_id = retrieve_fasta_id(info)
        seq_ids.setdefault(seq, []).append(fasta_id)

    with open(seq_path, 'w') as f_seq, open(id_path, 'w') as f_id:
        f_seq.write(str(len(seq_ids)) + "\n")
        f_id.write(str(len(seq_ids)) + "\n")

        # Make sure the two files are line-to-line mapping, write the seq and
        # ids in the same time.
        for seq, ids in seq_ids.items():
            f_seq.write(" ".join([str(len(seq)), seq]) + "\n")

            write_ids = [len(ids)] + ids
            f_id.write(" ".join([str(i) for i in write_ids]) + "\n")


def create_fasta_id_info_file(fasta_path, info_path):
    """
    Parse fasta file to make a fasta id information file.

    The output file format is as the following.

        [FASTA ID_0] [INFO_0]
        [FASTA ID_1] [INFO_1]
        ...
        [FASTA ID_n] [INFO_n]

    Args:
        fasta_path (str): The input fasta file
        info_path (str): The output fasta information file.
    """
    with open(info_path, 'w') as fout:
        for info, _ in read_fasta_file(fasta_path):
            fasta_id = retrieve_fasta_id(info)

            fout.write(" ".join([fasta_id, info]) + "\n")


class FastaSeqPath(object):
    """
    Present all file paths for the fasta file.
    """
    def __init__(self, raw_path, *, seq_path=None,
                 fasta_id_path=None, fasta_id_info_path=None):
        """
        Init the object.

        The object records all path information. It would create the related
        data strucutre.

        If the argument is None, the object will have a default path. The path
        is under temp folder. If you have these files, please specify them.
        """
        self._raw_path = os.path.abspath(raw_path)
        name = utility.retrieve_basename(self._raw_path)

        get_valid_path = lambda default_path, arg_path: \
            os.path.abspath(arg_path) if arg_path is not None else default_path

        self._seq_path = get_valid_path(
            utility.make_temp_path(name + "_seq.txt"), seq_path)
        self._fasta_id_path = get_valid_path(
            utility.make_temp_path(name + "_id.txt"), fasta_id_path)
        self._fasta_id_info_path = get_valid_path(
            utility.make_temp_path(name + "_id_info.txt"), fasta_id_info_path)

    @property
    def raw_path(self):
        return self._raw_path

    @property
    def seq_path(self):
        return self._seq_path

    @property
    def fasta_id_path(self):
        return self._fasta_id_path

    @property
    def fasta_id_info_path(self):
        return self._fasta_id_info_path


Sequence = collections.namedtuple('Sequence', ['raw_seq', 'fasta_ids'])


class Sequences(collections.abc.Mapping):
    """
    Present each sequences'info. A dict's wrapper
        key (int) presents the sequence id
        value (Sequence) presents the sequence information
            raw_seq presents the orignal seqeuence
            ids present the fasta ids of the sequence
    """
    def __init__(self, seqs):
        """
        Users can not call the init function directly.
        """
        self._seqs = seqs

    def __contains__(self, sid):
        return sid in self._seqs

    def __getitem__(self, sid):
        return self._seqs[sid]

    def __iter__(self):
        return iter(self._seqs)

    def __len__(self):
        return len(self._seqs)

    @staticmethod
    def read_file(seq_path, fasta_id_path, sequence_ids=None):
        """
        Create a dict to save the sequence and fasta ids.

        It's possible a unique seqeucne to map several fasta ids.

        Args:
            seq_path (str): the input sequence file path
            id_path (str): the input ids file path
            sequence_ids ([int]):  a list of sequence ids.
                If the parameter is None, it save all sequences from
                these files. Otherwise it only saves sequences which sequence
                ids appear in the list.

        Return:
            A Sequences object
        """
        seqs = dict()

        with open(seq_path, 'r') as fseq, open(fasta_id_path, 'r') as fid:
            seq_lines = fseq.read().splitlines()[1:]
            id_lines = fid.read().splitlines()[1:]

            for sid, (seq_line, ids_line) in enumerate(
                zip(seq_lines, id_lines)):
                if sequence_ids is None or sid in sequence_ids:
                    raw_seq = seq_line.split()[1]
                    fasta_ids = ids_line.split()[1:]
                    seqs[sid] = Sequence(raw_seq, fasta_ids)

        return Sequences(seqs)


class FastaIDInfos(collections.abc.Mapping):
    """
    Present each fasta id's information. A dict's wrapper.
        key (str) presents fasta id.
        value (str) presents fasta information.
    """
    def __init__(self, id_info):
        """
        Users can not call the init function directly.
        """
        self._id_info = id_info

    def __contains__(self, sid):
        return sid in self._id_info

    def __getitem__(self, sid):
        return self._id_info[sid]

    def __iter__(self):
        return iter(self._id_info)

    def __len__(self):
        return len(self._id_info)

    @staticmethod
    def read_file(path, fasta_ids=None):
        """
        Create a dictionary to save the information for each fasta id.

        Args:
            id_info_path (str): the input file path
            fasta_ids ([str]):  a list of fasta ids.
                If the parameter is None, it save all fasta id informations from
                the file. Otherwise it only saves information which fasta ids
                appear in the list.

        Return:
            a FastaIDinfos object.
        """
        id_info = dict()
        with open(path, 'r') as fin:
            for line in fin:
                words = line.split()

                fasta_id = words[0]
                fasta_info = " ".join(words[1:])

                if fasta_ids is None or fasta_id in fasta_ids:
                    id_info[fasta_id] = fasta_info

        return FastaIDInfos(id_info)


class FastaSeq(object):
    """
    A small helper class to collect two major fasta data structures.
    """
    def __init__(self, fasta_seq_path, *, sequence_ids=None, fasta_ids=None):
        self._seqs = Sequences.read_file(fasta_seq_path.seq_path,
                                         fasta_seq_path.fasta_id_path,
                                         sequence_ids)
        self._fasta_id_infos = FastaIDInfos.read_file(
            fasta_seq_path.fasta_id_info_path, fasta_ids)

    @property
    def seqs(self):
        return self._seqs

    @property
    def fasta_id_infos(self):
        return self._fasta_id_infos


def parse_fasta_file(path):
    """
    Parsing the input fasta file to create related data structures.

    Args:
        fasta_path (str): the input fasta file path

    Return:
        a FastaSeqPath object to point out the paths which contains parsed
        infomation for the input fasta file.
    """
    fasta_seq_path = FastaSeqPath(path)

    create_seq_fasta_id_file(fasta_seq_path.raw_path,
                             fasta_seq_path.seq_path,
                             fasta_seq_path.fasta_id_path)
    create_fasta_id_info_file(fasta_seq_path.raw_path,
                              fasta_seq_path.fasta_id_info_path)

    return fasta_seq_path
