# PyPCPE2

![travis-ci](https://travis-ci.org/yen3/pypcpe2.svg?branch=master)

* **The project is under construction.**
* The program can finds maximum common subseqences from DNA/protein seqeucnes.
  * It supports large number of seqeucnes comparasion (>= 100000).
  * The project wraps [pcpe2](https://github.com/yen3/pcpe2) as a python module.
    to speedup the compare time.

## Requirement

* Python 3
  * Python 3.4 or later
  * virtualenv
  * python-dev
* C++ compiler with C++11 support.
  * gcc 4.8.4 or later
  * clang 3.4 or later
* cmake


## Install

```
git clone  --recursive https://github.com/yen3/pypcpe2 pypcpe2
cd pypcpe2
virualenv -p python3 .env
source .env/bin/activate
python setup.py install
```


