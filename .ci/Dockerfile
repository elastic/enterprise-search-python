ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

WORKDIR /code/enterprise-search-python
COPY . .

RUN python -m pip install \
    --disable-pip-version-check \
    --no-cache-dir \
    -e . \
    -r dev-requirements.txt
