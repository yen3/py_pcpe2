FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y apt-utils && \
    apt-get install -y build-essential \
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
