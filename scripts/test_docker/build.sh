#!/usr/bin/env bash

function build_image
{
  cp Dockerfile Dockerfile_$1
  sed -i "s/3.4/$2/g" Dockerfile_$1
  docker build -t python$1 . -f Dockerfile_$1
  rm -rf Dockerfile_$1
}

build_image "34" "3.4"
build_image "35" "3.5"
build_image "36" "3.6"
