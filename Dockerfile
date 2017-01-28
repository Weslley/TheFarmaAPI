FROM python:3.5-alpine

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

RUN sh

ADD ./ /thefarmaapi

WORKDIR /thefarmaapi

EXPOSE 8000

# VOLUME [""]

RUN apk add post

RUN pip install -r requirements.txt
