FROM alpine/py3

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

RUN sh

ADD ./ /thefarmaapi

WORKDIR /thefarmaapi

EXPOSE 8000

VOLUME [""]

RUN pip install -r requirements.txt
