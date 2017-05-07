#/usr/bin/env bash

#export DEBIAN_FRONTEND=noninteractive

#rm -rf /var/lib/dpkg/lock
#apt-get update
#apt-get install -y python3 python3-dev gcc g++ python-virtualenv

#virtualenv -p python3 .env
#. .env/bin/activate

pip install -r requirements.txt

python3 setup.py develop
nosetests --detailed-errors --with-doctest -v

