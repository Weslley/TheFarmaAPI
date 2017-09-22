FROM mrlucascardoso/python-slim-postgres

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

ADD ./ /thefarmaapi

WORKDIR /thefarmaapi

EXPOSE 8000

RUN locale-gen pt_BR.UTF-8

RUN echo -e 'LC_ALL="pt_BR.UTF-8"\nLANG="pt_BR.UTF-8"\nLANGUAGE="pt_BR:pt"\n' > /etc/default/locale

RUN LANG='pt_BR.UTF-8'

RUN pip install -r requirements.txt
