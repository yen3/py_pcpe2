import os
import os.path
import logging
import argparse
import shutil

from pypcpe2 import utility

import pcpe2_core


class Setting(object):
    def __init__(self):
        self._temp_path = os.path.abspath(pcpe2_core.env_get_temp_path())
        self._buffer_size = pcpe2_core.env_get_buffer_size()
        self._io_buffer_size = pcpe2_core.env_get_io_buffer_size()
        self._output_min_len = pcpe2_core.env_get_min_output_length()
        self._compare_seq_size = pcpe2_core.env_get_compare_seq_size()
        self._thread_size = pcpe2_core.env_get_thread_size()
        self._clear_temp_files = True

        if not os.path.isdir(self._temp_path):
            os.makedirs(self._temp_path)

    def init_with_command_args(self, raw_args):
        if raw_args.parallel_tasks is not None:
            self.thread_size = int(raw_args.parallel_tasks)

        if raw_args.compare_size is not None:
            self.compare_seq_size = int(raw_args.compare_size)

        if raw_args.buffer_size is not None:
            self.buffer_size = int(raw_args.buffer_size) * 1024 * 1024

        if raw_args.temp_folder is not None:
            self.temp_path = os.path.abspath(raw_args.temp_folder)

        if raw_args.save_temps is True:
            self._clear_temp_files = False

    @property
    def temp_path(self):
        return self._temp_path

    @temp_path.setter
    def temp_path(self, path):
        self._temp_path = os.path.abspath(path)
        pcpe2_core.env_set_temp_path(self._temp_path)

        if not os.path.isdir(self._temp_path):
            os.makedirs(self._temp_path)

    @property
    def buffer_size(self):
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, set_size):
        self._buffer_size = set_size
        pcpe2_core.env_set_buffer_size(self._buffer_size)

    @property
    def io_buffer_size(self):
        return self._io_buffer_size

    @io_buffer_size.setter
    def io_buffer_size(self, set_size):
        self._io_buffer_size = set_size
        pcpe2_core.env_set_io_buffer_size(self._io_buffer_size)

    @property
    def output_min_len(self):
        return self._output_min_len

    @output_min_len.setter
    def output_min_len(self, set_size):
        self._output_min_len = set_size
        pcpe2_core.env_set_min_output_length(self._output_min_len)

    @property
    def compare_seq_size(self):
        return self._compare_seq_size

    @compare_seq_size.setter
    def compare_seq_size(self, set_size):
        self._compare_seq_size = set_size
        pcpe2_core.env_set_compare_seq_size(self._compare_seq_size)

    @property
    def thread_size(self):
        return self._thread_size

    @thread_size.setter
    def thread_size(self, set_size):
        self._thread_size = set_size
        pcpe2_core.env_set_thread_size(self._thread_size)

    @property
    def clear_temp_files(self):
        return self._clear_temp_files


_setting_instance = None
def setting():
    global _setting_instance
    if _setting_instance is not None:
        return _setting_instance

    _setting_instance = Setting()
    return _setting_instance


def parse_command_args(sys_argv):
    parser = argparse.ArgumentParser(description="PyPCPE2")
    parser.add_argument('input_path1', action='store', type=str,
                        nargs=1, help='input file 1')
    parser.add_argument('input_path2', action='store', type=str,
                        nargs=1, help='input file 2')
    parser.add_argument('-o', '--output', metavar="output_path",
                        dest="output_path", action='store',
                        type=str, help='output path')
    parser.add_argument('-r', '--output-human', metavar="output_human_path",
                        dest="output_human_path",
                        action='store', type=str, help='output path')
    parser.add_argument('-l', '--output-min-length', metavar='length',
                        dest="output_min_length", action='store', type=int,
                        help=("The minimum length of common subsequence to"
                              "output (Default value: 10)"))
    parser.add_argument('-p', '--parallel', metavar="size",
                        dest="parallel_tasks", action='store', type=int,
                        help=("The parallelism of the program"
                              "(Default value: the cpu counts including HT)"))
    parser.add_argument('-n', '--compare-size', metavar="seq_size",
                        dest="compare_size", action='store', type=int,
                        help=("The number of sequences to compare in one time."
                              "(Default value: 10000)"))
    parser.add_argument('-b', '--buffer-size', metavar="buffer_size",
                        dest="buffer_size", action='store', type=int,
                        help=("The buffer size for each thread's usage"
                              "(unit: Mbytes) (Default value: 100 Mbyes)"))
    parser.add_argument('-t', '--temp-folder', metavar="temp_folder_path",
                        dest="temp_folder", action='store', type=int,
                        help=("The folder to save temporary files during the"
                              "executiion (Default value: \"./temp\")"))
    parser.add_argument('--verbose', metavar="logging_path",
                        dest="verbose_output_path",
                        nargs='?', const="", action='store', type=str,
                        help=("Verbose mode. If the argument is empty, "
                              "it will output to the console"))
    parser.add_argument('--debug', metavar="logging_path",
                        dest="debug_output_path",
                        nargs='?', const="", action='store', type=str,
                        help=("Debug modeoutput. If the argument is empty, "
                              "it will output to the console"))
    parser.add_argument('--save-temps', action='store_true',
                        help=('Store all temporary files generated during '
                              'progress.'))


    return parser.parse_args(sys_argv[1:])


def init_logging(*, log_path=None, level=logging.WARNING):
    """
    Init the logging.

    Args:
        log_path (str): the log file path.
            If the argument is None, the logger print all messages in
            stdout/ stderr
        level (int): the logging level
    """
    # Set logging format string
    if level <= logging.DEBUG:
        format_str = "[%(levelname)s:%(filename)s:%(lineno)d]: %(message)s"
    else:
        format_str = "[%(levelname)s]: %(message)s"

    # Apply the setting
    logging.basicConfig(filename=None, level=level, format=format_str)
    pcpe2_core.init_logging(level)


def init_logging_with_command_args(raw_args):
    """
    Init the logging facility by parsing the command arguments

    It's a wrapper for `init_logging`. Just pass the correct argument to the
    function and do nothing.
    """
    check_empty = lambda x: x if x != '' else None
    if raw_args.verbose_output_path is not None:
        init_logging(log_path=check_empty(raw_args.verbose_output_path),
                     level=logging.INFO)

    if raw_args.debug_output_path is not None:
        init_logging(log_path=check_empty(raw_args.debug_output_path),
                     level=logging.DEBUG)


def parse_input_output_paths(raw_args):
    """
    Get input/ output paths by parsing the command arguments

    Return:
        a dict to present the input/ output paths which are needed.

        key                  value      meaning
        "x_input_path"       str        input file path
        "y_input_path"       str        input file path
        "output_path"        str        output file path
        "output_human_path"  str        output human-redable file path.
                                        The value could be None
    """
    program_path = dict()
    program_path['x_input_path'] = os.path.abspath(raw_args.input_path1[0])
    program_path['y_input_path'] = os.path.abspath(raw_args.input_path2[0])

    if raw_args.output_path is not None:
        program_path['output_path'] = os.path.abspath(raw_args.output_path)
    else:
        output_fn = "{x}_{y}_comsubseq.txt".format(
            x=utility.retrieve_basename(program_path['x_input_path']),
            y=utility.retrieve_basename(program_path['y_input_path']))

        program_path['output_path'] = os.path.abspath(os.path.join(".",
                                                                   output_fn))

    if raw_args.output_human_path is not None:
        program_path['output_human_path'] = os.path.abspath(
            raw_args.output_human_path)
    else:
        output_human_fn = "{output_base}_human.txt".format(
            output_base=utility.retrieve_basename(program_path['output_path']))
        program_path['output_human_path'] = os.path.abspath(os.path.join(
            ".", output_human_fn))

    return program_path


def init_env(sys_argv):
    """
    Read command argument and init the program environment.

    The function inits all environment variables  and reurn the input and
    output paths.

    Args:
        sys_argv ([str]): the command line arguments

    Return:
        a dict to present the input/ output paths which are needed.
            See `parse_input_output_paths` function to get details
    """
    # Parse command line arugments
    raw_args = parse_command_args(sys_argv)
    print(raw_args)

    # Set the environment varibles
    setting().init_with_command_args(raw_args)

    # Init logging with command line setting
    init_logging_with_command_args(raw_args)

    # Parse the input/ output paths
    program_path = parse_input_output_paths(raw_args)
    print(program_path)

    return program_path

def clean_env():
    if setting().clear_temp_files == True:
        shutil.rmtree(setting().temp_path)

