import unittest
import os.path

import pcpe2_core

from pypcpe2.env import env


class TestPCPE2Core(unittest.TestCase):
    def test_env_temp_path(self):
        self.assertEqual(os.path.abspath("./temp"),
                         os.path.abspath(pcpe2_core.env_get_temp_path()))

        pcpe2_core.env_set_temp_path(env().temp_path)
        self.assertEqual(pcpe2_core.env_get_temp_path(), env().temp_path)

    def test_env_min_length(self):
        saved_length = pcpe2_core.env_get_min_output_length()

        set_length = 9
        pcpe2_core.env_set_min_output_length(set_length)
        self.assertEqual(pcpe2_core.env_get_min_output_length(), set_length)

        pcpe2_core.env_set_min_output_length(saved_length)

