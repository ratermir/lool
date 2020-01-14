FROM alpine:latest

# add all necessary diles
ADD content/bin/ /usr/local/bin/
ADD content/fonts/ /usr/share/fonts/
ADD content/app/ /app/
ADD content/entrypoint.sh /

# install python3 
RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
\
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel xmltodict && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
\
    echo "**** install libreoffice and related ****" && \
    apk add --no-cache bash mc openjdk8-jre libreoffice && \
\
    echo "**** clean-up libreoffice parts that seem to be unnecessary ****" && \
    cd /usr/lib/libreoffice/share && \
    rm -rf wizards xslt gallery template autocorr basic config emojiconfig labels theme_definitions palette autotext Scripts calc filter psprint tipoftheday && \
    cd /usr/lib/libreoffice/program/ && \
    rm -rf classes opengl shell wizards && \
    rm libmysql_jdbclo.so libmysqlclo.so postgresql-sdbc.ini libpostgresql-sdbclo.so libpostgresql-sdbc-impllo.so && \
    rm libsclo.so libsdlo.so libchartcontrollerlo.so libchartcorelo.so libswuilo.so libdict_??.so libdbulo.so libdbaselo.so libdbalo.so && \
    rm libdbahsqllo.so libdbpool2.so libdbaxmllo.so liblocaledata_euro.so liblocaledata_others.so libcuilo.so libdeploymentgui.so && \
\
    echo "**** install libreoffice and related ****" && \
    pip install pystache && \
    apk add py3-yaml && \
    addgroup app && \
    adduser -u 1001 -G app -h /app -s /dev/null -D app && \
    mkdir -p /app && \
    chown -R app:app /app && chmod +s /app && \
    echo "**** performing additional changes ****" && \
    chmod +x /entrypoint.sh
    



USER app
ENTRYPOINT /entrypoint.sh
