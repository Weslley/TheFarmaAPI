FROM mrlucascardoso/python-slim-postgres

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

ADD ./ /thefarmaapi

WORKDIR /thefarmaapi

EXPOSE 8000

RUN locale-gen pt_BR.UTF-8

ENV LC_ALL pt_BR.UTF-8

RUN pip install -r requirements.txt
