FROM ubuntu:14.04.4 as base
RUN mkdir /app
WORKDIR /app

FROM base as build
COPY ./bootstrap.sh /app
RUN ./bootstrap.sh
COPY . /app
ENTRYPOINT ["./ubuntu-config-tool"]

FROM build as tests
ENV PYTHONPATH="/app"
CMD python3 -m unittest tests/*
