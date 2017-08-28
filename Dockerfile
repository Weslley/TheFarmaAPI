FROM python:3.5-slim

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

ADD ./ /thefarmaapi

WORKDIR /thefarmaapi

EXPOSE 8000

RUN apt-get update

RUN apt-get install postgresql-contrib openssl -y

RUN apt-get install git -y

RUN pip install -r requirements.txt
