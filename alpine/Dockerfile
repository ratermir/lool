FROM alpine:latest

RUN \
    apk add --no-cache bash openjdk8-jre libreoffice  mc && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /usr/lib/libreoffice/share/wizards && \
    rm -rf /usr/lib/libreoffice/share/gallery && \
    rm -rf /usr/lib/libreoffice/share/template && \
    rm -rf /usr/lib/libreoffice/program/classes && \
    rm -rf /usr/lib/libreoffice/share/config
    

ADD content/bin/ /usr/local/bin/
