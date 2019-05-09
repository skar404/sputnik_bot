FROM python:3.7-alpine

WORKDIR /app

ADD requirements.txt .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && pip install --upgrade pip \
 && pip install cython \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .build-deps

ADD . /app
