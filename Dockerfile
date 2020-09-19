FROM ubuntu:14.04.4
RUN mkdir /app
COPY . /app
WORKDIR /app

RUN ./bootstrap.sh
