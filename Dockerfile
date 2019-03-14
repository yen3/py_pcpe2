ARG PYTHON_VERSION=3.6

FROM python:${PYTHON_VERSION}-stretch

ADD . /app

WORKDIR /app

RUN pip install --no-cache-dir -r ./requirements.txt \
    && python3 setup.py develop

CMD ["nosetests", "--detailed-errors", "--with-doctest", "-v"]

