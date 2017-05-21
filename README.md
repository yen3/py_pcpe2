# PyPCPE2

![travis-ci](https://travis-ci.org/yen3/pypcpe2.svg?branch=master)

* **The project is under construction.**
* The program can finds maximum common subseqences from DNA/protein seqeucnes.
  * It supports large number of seqeucnes comparasion (>= 100000).
  * The project wraps [pcpe2](https://github.com/yen3/pcpe2) as a python module.
    to speedup the compare time.
* The original design is from Professor [Guang-Wu Chen](http://rcevi.cgu.edu.tw/files/14-1065-4045,r639-1.php).

## Requirement

* Python 3
  * Python 3.4 or later
  * virtualenv
  * python-dev
* C++ compiler with C++11 support.
  * gcc 4.8.4 or later
  * clang 3.4 or later

## Install

```
git clone  --recursive https://github.com/yen3/pypcpe2 pypcpe2
cd pypcpe2
virualenv -p python3 .env
source .env/bin/activate
python setup.py install
```

## Usage

```
$ max_comsubseq.py --help
usage: max_comsubseq.py [-h] [-o output_path] [-r output_human_path]
                        [-l length] [-p size] [-n seq_size] [-b buffer_size]
                        [-t temp_folder_path] [--verbose [logging_path]]
                        [--debug [logging_path]] [--save-temps]
                        input_path1 input_path2

PyPCPE2

positional arguments:
  input_path1           input file 1
  input_path2           input file 2

optional arguments:
  -h, --help            show this help message and exit
  -o output_path, --output output_path
                        output path
  -r output_human_path, --output-human output_human_path
                        output path
  -l length, --output-min-length length
                        The minimum length of common subsequence tooutput
                        (Default value: 10)
  -p size, --parallel size
                        The parallelism of the program(Default value: the cpu
                        counts including HT)
  -n seq_size, --compare-size seq_size
                        The number of sequences to compare in one
                        time.(Default value: 10000)
  -b buffer_size, --buffer-size buffer_size
                        The buffer size for each thread's usage(unit: Mbytes)
                        (Default value: 100 Mbyes)
  -t temp_folder_path, --temp-folder temp_folder_path
                        The folder to save temporary files during
                        theexecutiion (Default value: "./temp")
  --verbose [logging_path]
                        Verbose mode. If the argument is empty, it will output
                        to the console
  --debug [logging_path]
                        Debug modeoutput. If the argument is empty, it will
                        output to the console
  --save-temps          Store all temporary files generated during progress.
```
