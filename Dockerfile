FROM mrlucascardoso/python-slim-postgres

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

ADD ./ /thefarmaapi

WORKDIR /thefarmaapi

EXPOSE 8000

RUN pip install -r requirements.txt
