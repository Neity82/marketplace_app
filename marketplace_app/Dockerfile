FROM python:3.8-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

COPY . .

RUN apk add --update --no-cache --virtual .tmp-build-deps \
     gcc libc-dev linux-headers postgresql-dev tree vim

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
