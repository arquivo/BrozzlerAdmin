# https://github.com/ukwa/docker-warcprox
FROM python:3.6-alpine

MAINTAINER steranin

RUN export LC_ALL=C.UTF-8 && \
    apk add --update build-base libffi libffi-dev openssl openssl-dev git && \
    pip install 'git+https://github.com/internetarchive/warcprox.git' && \
    apk del build-base libffi-dev openssl-dev

EXPOSE 9000 

VOLUME ["/warcs", "/db", "/ca"]

#ENTRYPOINT ["warcprox", "--address", "0.0.0.0", "--port", "8888"]

CMD warcprox --rethinkdb-servers 172.17.0.1:28015 --rethinkdb-db brozzler --rethinkdb-big-table -p 9000 -b 0.0.0.0 --base32 -z --rollover-idle-time 3600 2>&1 | tee /logs
