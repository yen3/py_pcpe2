import os
import os.path
import enum

test_data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')
test_output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testoutput')

if os.path.isdir(test_output_folder) is False:
    os.mkdir(test_output_folder)
