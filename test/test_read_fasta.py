import unittest
import os
import os.path

import test.env

class TestReadFASTA(unittest.TestCase):
	def test_env(self):
		self.assertTrue(os.path.isdir(test.env.test_data_folder))
		self.assertTrue(os.path.isdir(test.env.test_output_folder))
