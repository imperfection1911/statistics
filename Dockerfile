FROM python:3.4
MAINTAINER Anton Aksenov <imperfection1911@gmail.com>
RUN pip install psycopg2-binary paramiko
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install postgresql-client
COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh
WORKDIR /app
ENTRYPOINT /entrypoint.sh