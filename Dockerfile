FROM python:3.6-stretch

ADD . /app

WORKDIR /app

RUN pip install --no-cache-dir -r ./requirements.txt \
    && python3 setup.py develop

CMD ["nosetests", "--detailed-errors", "--with-doctest", "-v"]

