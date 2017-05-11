import shutil
import os.path

from pypcpe2.env import setting

def retrieve_basename(path):
    """
    Get the basename without extension

    Example:
    >>> retrieve_basename('/Users/user/test.txt')
    'test'
    >>> retrieve_basename('/Users/user/test')
    'test'
    """
    return os.path.splitext(os.path.basename(path))[0]

def make_temp_path(filename):
    """
    Return a temp path based on the pass filename

    Args:
        filename (str): the temp filename

    Return:
        A str presents the temp path
    """
    return os.path.join(setting().temp_path, os.path.basename(filename))


def merge_file(input_paths, output_path):
    """
    Merge files into one file.

    Args:
        input_paths ([str]): list of input paths
        output_path (str): the output file path
    """
    with open(output_path, 'wb') as fout:
        for path in input_paths:
            with open(path, 'rb') as fin:
                shutil.copyfileobj(fin, fout)
