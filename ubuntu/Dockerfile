FROM ubuntu:19.04

RUN \
    apt-get -y update && \
    apt-get -y install openjdk-8-jre mc python3 libreoffice-core libreoffice-writer --no-install-recommends && \
    ln -s /usr/bin/python3 /usr/bin/python

ADD content/bin/ /usr/local/bin/
