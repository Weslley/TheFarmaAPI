FROM mrlucascardoso/python-slim-postgres

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

ADD ./ /thefarmaapi

WORKDIR /thefarmaapi

EXPOSE 8000

RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

RUN apt-get install python-dev graphviz libgraphviz-dev pkg-config

RUN pip install -r requirements.txt
