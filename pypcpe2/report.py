from pypcpe2 import read_fasta

def make_report(x_seqfile, y_seqfile, seq_result,
                output_path, human_output_path):
    x = read_fasta.SeqFileInfo(x_seqfile)
    y = read_fasta.SeqFileInfo(y_seqfile)

