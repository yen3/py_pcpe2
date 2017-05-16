import unittest
import os
import os.path
import shlex
import logging

import test.env

from pypcpe2 import comsubseq
from pypcpe2 import env
from pypcpe2 import utility


class TestEnv(unittest.TestCase):
    def setUp(self):
        self.test_data_folder = os.path.join(test.env.test_data_folder,
                                             "env")
        self.test_output_folder = os.path.join(test.env.test_output_folder,
                                               "env")
        if not os.path.isdir(self.test_output_folder):
            os.makedirs(self.test_output_folder)

        self.saved_temp_path = env.setting().temp_path
        env.setting().temp_path = self.test_output_folder
        self.temp_path = env.setting().temp_path

        self.saved_setting = env.Setting()
        self.saved_setting._temp_path = env.setting()._temp_path
        self.saved_setting._buffer_size = env.setting()._buffer_size
        self.saved_setting._io_buffer_size = env.setting()._io_buffer_size
        self.saved_setting._output_min_len = env.setting()._output_min_len
        self.saved_setting._compare_seq_size = env.setting()._compare_seq_size
        self.saved_setting._thread_size = env.setting()._thread_size
        self.saved_setting._clear_temp_files = env.setting()._clear_temp_files

    def tearDown(self):
        env.setting().temp_path = self.saved_temp_path

        env.setting()._temp_path =  self.saved_setting._temp_path
        env.setting()._buffer_size =  self.saved_setting._buffer_size
        env.setting()._io_buffer_size =  self.saved_setting._io_buffer_size
        env.setting()._output_min_len =  self.saved_setting._output_min_len
        env.setting()._compare_seq_size =  self.saved_setting._compare_seq_size
        env.setting()._thread_size =  self.saved_setting._thread_size
        env.setting()._clear_temp_files =  self.saved_setting._clear_temp_files

    def test_parse_command_arguments(self):
        sys_argv = shlex.split("max_comsubseq.py test1.txt test2.txt")
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.input_path1[0], "test1.txt")
        self.assertEqual(raw_args.input_path2[0], "test2.txt")

    def test_parse_command_arguments_2(self):
        # case 1
        sys_argv = shlex.split(
            ("max_comsubseq.py test1.txt test2.txt --verbose"))
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.verbose_output_path, "")
        self.assertEqual(raw_args.debug_output_path, None)

        # case 2
        sys_argv = shlex.split(
            ("max_comsubseq.py test1.txt test2.txt --verbose --debug"))
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.verbose_output_path, "")
        self.assertEqual(raw_args.debug_output_path, "")

        # case 3
        temp_log_path = utility.make_temp_path("test_log.txt")
        sys_argv = shlex.split(
            ("max_comsubseq.py test1.txt test2.txt --verbose=" + \
             temp_log_path + "  --debug=" + temp_log_path))
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.verbose_output_path, temp_log_path)
        self.assertEqual(raw_args.debug_output_path, temp_log_path)

    def test_parse_input_output_path(self):
        sys_argv = shlex.split("max_comsubseq.py test1.txt test2.txt")
        raw_args = env.parse_command_args(sys_argv)

        program_path = env.parse_input_output_paths(raw_args)
        self.assertEqual(program_path['x_input_path'],
                         os.path.abspath('test1.txt'))
        self.assertEqual(program_path['y_input_path'],
                         os.path.abspath('test2.txt'))
        self.assertEqual(program_path['output_path'],
                         os.path.abspath('test1_test2_comsubseq.txt'))
        self.assertEqual(program_path['output_human_path'],
                         os.path.abspath('test1_test2_comsubseq_human.txt'))

    def test_parse_input_output_path_2(self):
        sys_argv = shlex.split(
            "max_comsubseq.py test1.txt test2.txt -o test3.txt")
        raw_args = env.parse_command_args(sys_argv)

        program_path = env.parse_input_output_paths(raw_args)
        self.assertEqual(program_path['x_input_path'],
                         os.path.abspath('test1.txt'))
        self.assertEqual(program_path['y_input_path'],
                         os.path.abspath('test2.txt'))
        self.assertEqual(program_path['output_path'],
                         os.path.abspath('test3.txt'))
        self.assertEqual(program_path['output_human_path'],
                         os.path.abspath('test3_human.txt'))

    def test_parse_input_output_path_2(self):
        sys_argv = shlex.split(
            ("max_comsubseq.py test1.txt test2.txt -o test3.txt "
             "-r test_human.txt"))
        raw_args = env.parse_command_args(sys_argv)

        program_path = env.parse_input_output_paths(raw_args)
        self.assertEqual(program_path['x_input_path'],
                         os.path.abspath('test1.txt'))
        self.assertEqual(program_path['y_input_path'],
                         os.path.abspath('test2.txt'))
        self.assertEqual(program_path['output_path'],
                         os.path.abspath('test3.txt'))
        self.assertEqual(program_path['output_human_path'],
                         os.path.abspath('test_human.txt'))

    def test_parse_input_output_path_3(self):
        sys_argv = shlex.split(
            ("max_comsubseq.py test1.txt test2.txt -r test_human.txt"))
        raw_args = env.parse_command_args(sys_argv)

        program_path = env.parse_input_output_paths(raw_args)
        self.assertEqual(program_path['x_input_path'],
                         os.path.abspath('test1.txt'))
        self.assertEqual(program_path['y_input_path'],
                         os.path.abspath('test2.txt'))
        self.assertEqual(program_path['output_path'],
                         os.path.abspath('test1_test2_comsubseq.txt'))
        self.assertEqual(program_path['output_human_path'],
                         os.path.abspath('test_human.txt'))

    def test_setting_temp_path(self):
        sys_argv = shlex.split(
            "max_comsubseq.py test1.txt test1.txt --temp-folder ./test_pcpe2")
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.temp_folder, "./test_pcpe2")

        setting = env.Setting()
        setting.init_with_command_args(raw_args)
        self.assertEqual(setting.temp_path, os.path.abspath("./test_pcpe2"))

    def test_setting_output_min_length(self):
        sys_argv = shlex.split(
            "max_comsubseq.py test1.txt test1.txt -l 10")
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.output_min_length, 10)

        setting = env.Setting()
        setting.init_with_command_args(raw_args)
        self.assertEqual(setting.output_min_len, 10)

    def test_setting_parallel(self):
        sys_argv = shlex.split(
            "max_comsubseq.py test1.txt test1.txt -p 3")
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.parallel_tasks, 3)

        setting = env.Setting()
        setting.init_with_command_args(raw_args)
        self.assertEqual(setting.thread_size, 3)

    def test_setting_parallel(self):
        sys_argv = shlex.split(
            "max_comsubseq.py test1.txt test1.txt -n 9999")
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.compare_size, 9999)

        setting = env.Setting()
        setting.init_with_command_args(raw_args)
        self.assertEqual(setting.compare_seq_size, 9999)

    def test_setting_buffer_size(self):
        sys_argv = shlex.split(
            "max_comsubseq.py test1.txt test1.txt -b 99")
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.buffer_size, 99)

        setting = env.Setting()
        setting.init_with_command_args(raw_args)
        self.assertEqual(setting.buffer_size, 99 * 1024 * 1024)

    def test_setting_saved_temp(self):
        sys_argv = shlex.split(
            "max_comsubseq.py test1.txt test1.txt --save-temps")
        raw_args = env.parse_command_args(sys_argv)

        self.assertEqual(raw_args.save_temps, True)

        setting = env.Setting()
        setting.init_with_command_args(raw_args)
        self.assertEqual(setting.clear_temp_files, False)

    def test_clean_env(self):
        env.clean_env()

        self.assertEqual(os.path.exists(env.setting().temp_path), False)
