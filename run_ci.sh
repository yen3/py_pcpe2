#/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y python3 python3-dev gcc g++ python-virtualenv virtualenv -p python3 .env
source .env/bin/activate

pip install -r requirements.txt

python setup.py develop
nosetests --detailed-errors --with-doctest -v

