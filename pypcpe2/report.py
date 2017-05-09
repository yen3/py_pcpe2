"""
Generate final report for maximum common subsequences

Users could call `make_report` function to generate report.
"""
from pypcpe2 import read_fasta
from pypcpe2 import comsubseq


class Record(object):
    """
    Common Subseqence's information

    It collects information for output.
    """
    def __init__(self, css, x_fasta_seq, y_fasta_seq):
        self.x_loc = css.x_loc
        self.y_loc = css.y_loc
        self.raw_seq_length = css.length

        x_raw_seq = x_fasta_seq.seqs[css.x].raw_seq
        self.raw_seq = x_raw_seq[self.x_loc: self.x_loc + self.raw_seq_length]

        self.x_fasta_id_infos = {
            fid: x_fasta_seq.fasta_id_infos[fid]
            for fid in x_fasta_seq.seqs[css.x].fasta_ids}

        self.y_fasta_id_infos = {
            fid: y_fasta_seq.fasta_id_infos[fid]
            for fid in y_fasta_seq.seqs[css.y].fasta_ids}

    def __repr__(self):
        s = ("Record(raw_seq=\"{raw_seq}\", "
             "raw_seq_length={raw_seq_length}, "
             "x_loc={x_loc}, y_loc={y_loc}, "
             "x_fasta_id_infos={x_fasta_id_infos}, "
             "y_fasta_id_infos={y_fasta_id_infos})")

        return s.format(**self.__dict__)


class Reporter(object):
    """
    Make report about common subsequences.
    """
    def __init__(self, x_fasta_seq_path, y_fasta_seq_path,
                 comsubseq_path):
        comsubseqs = comsubseq.read_comsubseq_file(comsubseq_path)

        x_sids = {css.x for css in comsubseqs}
        x_fasta_seq = read_fasta.FastaSeq(x_fasta_seq_path, sequence_ids=x_sids)

        y_sids = {css.y for css in comsubseqs}
        y_fasta_seq = read_fasta.FastaSeq(y_fasta_seq_path, sequence_ids=y_sids)

        self.records = [Record(css, x_fasta_seq, y_fasta_seq)
                        for css in comsubseqs]

    def make_report(self, output_path):
        """
        Generate machine-readable report for the comparsion result.

        The format of the file is a list of records.  Each record is seperated
        by `\n`. Each record contains

        [length] [comsubseq] [x_fasta_id] [y_fasta_id] [x_loc] [y_loc]

        Example:

            ```
            6 BCDEFG 9999999994 9999999992 1 0
            7 CDEFGHI 9999999995 9999999991 2 0
            ```

        Args:
            output_path (str): the output path to save the result.
        """
        with open(output_path, 'w') as fout:
            for record in self.records:
                fasta_ids = ((x, y) for x in record.x_fasta_id_infos.keys()
                             for y in record.y_fasta_id_infos.keys())

                for x_fasta_id, y_fasta_id in fasta_ids:
                    write_segs = [record.raw_seq_length, record.raw_seq,
                                  x_fasta_id, y_fasta_id,
                                  record.x_loc, record.y_loc]

                    fout.write(" ".join([str(w) for w in write_segs]) + "\n")


    def make_human_report(self, output_path):
        """
        Generate human-readable report for the comparsion result.

        The file format contains a list of records. Each record is seperated by
        `===...===`.

        The record format is

            ```
            [length] [comsubseq]
            x: [x_fasta_id_0] [x_fasta_id_1] ...
            x_loc: [x_loc]
            y: [y_fasta_id_0] [y_fasta_id_1] ...
            y_loc: [y_loc]

            [x0 - [x_fasta_id_0]]: [x_fasta_id_0_info]
            [x1 - [x_fasta_id_1]]: [x_fasta_id_1_info]
            ...
            [y0 - [y_fasta_id_0]]: [y_fasta_id_0_info]
            [y1 - [y_fasta_id_1]]: [y_fasta_id_1_info]
            ...

            ==================================================
            ```

        Example:

            ```
            6 BCDEFG
            x: 9999999998 9999999997 9999999996
            x_loc: 1
            y: 9999999993 9999999992
            y_loc: 0

            [x0 - 9999999998]: >gi|9999999998|gb|AOS87590|pypcpe2 test sequence2
            [x1 - 9999999997]: >gi|9999999997|gb|AOS87590|pypcpe2 test sequence3
            [x2 - 9999999996]: >gi|9999999996|gb|AOS87590|pypcpe2 test sequence4

            [y0 - 9999999993]: >gi|9999999993|gb|AOS87590|pypcpe2 test sequence7
            [y1 - 9999999992]: >gi|9999999992|gb|AOS87590|pypcpe2 test sequence8

            ==================================================
            ```

        Args:
            output_path (str): the output path to save the result.
        """
        with open(output_path, 'w') as fout:
            for record in self.records:
                fout.write(" ".join(
                    [str(record.raw_seq_length), record.raw_seq]) + "\n")
                fout.write("x: " + " ".join(
                    record.x_fasta_id_infos.keys()) + "\n")
                fout.write("x_loc: " + str(record.x_loc) + "\n")
                fout.write("y: " + " ".join(
                    record.y_fasta_id_infos.keys()) + "\n")
                fout.write("y_loc: " + str(record.y_loc) + "\n")

                fout.write("\n")
                for index, (fasta_id, info) in enumerate(
                        record.x_fasta_id_infos.items()):
                    fout.write("[x{n} - {fasta_id}]: {fasta_id_info}\n".format(
                        n=index, fasta_id=fasta_id, fasta_id_info=info))

                fout.write("\n")
                for index, (fasta_id, info) in enumerate(
                        record.y_fasta_id_infos.items()):
                    fout.write("[y{n} - {fasta_id}]: {fasta_id_info}\n".format(
                        n=index, fasta_id=fasta_id, fasta_id_info=info))


                fout.write(("\n========================"
                            "==========================\n"))


def make_report(x_fasta_seq_path, y_fasta_seq_path, comsubseq_path,
                output_path, human_output_path):
    """
    Generate report for maximum common subsequences

    Args:
        x_fasta_seq_path (FastaSeqPath): the input file paths
        y_fasta_seq_path (FastaSeqPath): the input file paths
        comsubseq_path (str): the compare result path
        output_path (str): the major output path for machine-readable file
        human_output_path (str): the output path for human-readable file
    """
    reporter = Reporter(x_fasta_seq_path, y_fasta_seq_path, comsubseq_path)

    reporter.make_report(output_path)
    reporter.make_human_report(human_output_path)
