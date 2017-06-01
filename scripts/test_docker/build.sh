#!/usr/bin/env bash

cp Dockerfile Dockerfile_3_4
sed -i 's/3.4/3.4/g' Dockerfile_3_4

cp Dockerfile Dockerfile_3_5
sed -i 's/3.4/3.5/g' Dockerfile_3_5

cp Dockerfile Dockerfile_3_6
sed -i 's/3.4/3.6/g' Dockerfile_3_6


docker build -t python34 . -f Dockerfile_3_4
docker build -t python35 . -f Dockerfile_3_5
docker build -t python36 . -f Dockerfile_3_6

rm -rf Dockerfile_3_4
rm -rf Dockerfile_3_5
rm -rf Dockerfile_3_6
