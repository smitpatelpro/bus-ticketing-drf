FROM python:3.11.4-alpine3.18

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers python3-dev postgresql-dev build-base python3-dev


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
