FROM tiangolo/uvicorn-gunicorn:python3.6

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app
