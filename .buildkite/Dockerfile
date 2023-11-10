ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

WORKDIR /code/enterprise-search-python

COPY dev-requirements.txt .

ENV AIOHTTP_NO_EXTENSIONS=1

RUN python -m pip install \
    --disable-pip-version-check \
    --no-cache-dir \
    -r dev-requirements.txt

COPY . .
