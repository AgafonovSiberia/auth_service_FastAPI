FROM python:3.10-slim-bullseye

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
COPY alembic.ini .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY .. .


