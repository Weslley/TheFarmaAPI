#!/bin/bash

/usr/local/bin/docker-compose -f /root/apps/thefarmaapi/docker-compose.yml run certbot renew\
&& /usr/local/bin/docker-compose -f /root/apps/thefarmaapi/docker-compose.yml kill -s SIGHUP nginx

