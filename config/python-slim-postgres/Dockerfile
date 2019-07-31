FROM python:3.5-slim

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

RUN apt-get update

RUN apt-get install -y wget

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update

RUN apt-get install -y postgresql-contrib-9.6 libpq-dev postgresql-client-9.6 openssl git gcc

RUN apt-get install -y libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev

RUN apt-get install -y libgraphviz-dev graphviz graphviz-dev pkg-config
