FROM python:3.4

RUN git clone  --recursive https://github.com/yen3/pypcpe2 pypcpe2
WORKDIR /pypcpe2
COPY ./internal/test_docker.sh test_docker.sh

CMD ["python3"]

# vim: ft=dockerfile
