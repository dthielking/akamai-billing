FROM mysql:latest
RUN apt-get -y install bash && rm -rf /var/lib/apt/*
COPY akamaibilling.sql /docker-entrypoint-initdb.d/
