FROM ubuntu:16.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:ubuntu-toolchain-r/test

RUN apt-get update RUN apt-get upgrade -y
RUN apt-get install -y g++ \
                       g++-6 \
                       cmake \
                       git \
                       python3 \
                       python3-pip \
                       python3-dev

RUN git clone  --recursive https://github.com/yen3/pypcpe2 pypcpe2
WORKDIR /pypcpe2
COPY ./internal/test_docker.sh test_docker.sh

CMD ["python3"]

# vim: ft=dockerfile
