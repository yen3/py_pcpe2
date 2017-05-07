from pypcpe2 import read_fasta
from pypcpe2 import comsubseq


class Reporter(object):
    def __init__(x_seqpath, y_seqpath, comsubseq_path):
        self.x_seqpath = x_seqpath
        self.y_seqpath = y_seqpath
        self.comsubseq_path = comsubseq_path

        self.x_seqinfo = read_fasta.SeqFileInfo(x_seqfile)
        self.y_seqinfo = read_fasta.SeqFileInfo(y_seqfile)
        self.comsubseqs = comsubseq.read_comsubseq_file(self.comsubseq_path)


def make_human_report(x_seqinfo, y_seqinfo, seqs, output_path):
    with open(output_path, 'w') as fout:
        for seq in seqs:
            x_raw_str = x_seqinfo.seq_info[seq.x].seq

            x_ids = x_seqinfo.seq_info[seq.x].ids
            y_ids = y_seqinfo.seq_info[seq.y].ids

            length = seq.length
            subseq = x_raw_str[seq.x_loc:seq.x_loc+seq.length]

            fout.write(" ".join([str(length), subseq]) + "\n")
            fout.write("x: " + " ".join(x_ids) + "\n")
            fout.write("x_loc: " + str(seq.x_loc) + "\n")
            fout.write("y: " + " ".join(y_ids) + "\n")
            fout.write("y_loc: " + str(seq.y_loc) + "\n")

            fout.write("\n")
            for n, xid in enumerate(x_ids):
                fout.write("[x{n} - {xid}]: {fasta_id_info}\n".format(
                    n=n, xid=xid, fasta_id_info=x_seqinfo.id_info[xid]))

            fout.write("\n")
            for n, yid in enumerate(y_ids):
                fout.write("[y{n} - {yid}]: {fasta_id_info}\n".format(
                    n=n, yid=yid, fasta_id_info=y_seqinfo.id_info[yid]))

            fout.write("\n==================================================\n")


def make_machine_report(x_seqinfo, y_seqinfo, seqs, output_path):
    with open(output_path, 'w') as fout:
        fout.write("# len substr x_fasta y_fasta x_loc y_loc\n")
        for seq in seqs:
            x_raw_str = x_seqinfo.seq_info[seq.x].seq

            x_ids = x_seqinfo.seq_info[seq.x].ids
            y_ids = y_seqinfo.seq_info[seq.y].ids

            for xid in x_ids:
                for yid in y_ids:
                    sub = x_raw_str[seq.x_loc:seq.x_loc+seq.length]
                    record = [seq.length, sub, xid, yid, seq.x_loc, seq.y_loc]
                    fout.write("\t".join([str(r) for r in record]) + "\n")


def make_report(x_seqfile, y_seqfile, seq_result,
                output_path, human_output_path):
    x = read_fasta.SeqFileInfo(x_seqfile)
    y = read_fasta.SeqFileInfo(y_seqfile)

    seqs = comsubseq.read_comsubseq_file(seq_result)

    make_machine_report(x, y, seqs, output_path)
    make_human_report(x, y, seqs, human_output_path)

