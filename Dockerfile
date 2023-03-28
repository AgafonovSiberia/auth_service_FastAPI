FROM python:3.11-buster as builder
ENV VIRTUAL_ENV=/opt/venv
ENV CODE_PATH=/src
RUN pip3 install --no-cache-dir poetry==1.4.0
RUN python3 -m venv $VIRTUAL_ENV
WORKDIR $CODE_PATH
COPY poetry.lock pyproject.toml ${CODE_PATH}/
RUN python3 -m poetry --without=win export -f requirements.txt | $VIRTUAL_ENV/bin/pip install -r /dev/stdin

FROM python:3.11-slim-buster
ENV VIRTUAL_ENV=/opt/venv
ENV CODE_PATH=/src
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR $CODE_PATH


COPY ./src .