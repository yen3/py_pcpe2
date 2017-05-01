import os.path
from pypcpe2.env import env

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
    return os.path.join(env().temp_path, os.path.basename(filename))
