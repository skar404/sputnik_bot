FROM python:3.7-alpine

RUN \
    apk --no-cache add --update gcc python3-dev build-base && \
    rm -rf /var/cache/apk/*

WORKDIR /app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . /app

CMD ["gunicorn", "manage:init", "-c", "gunicorn_conf.py"]