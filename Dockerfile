FROM ubuntu:16.04

# This is needed for flow, and the weirdos that built it in ocaml:
RUN apt-get update && apt-get install -y python3 python3-dev gcc g++

RUN useradd jenkins --shell /bin/bash --create-home
USER jenkins
