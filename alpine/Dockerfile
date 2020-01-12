FROM alpine:latest

RUN \
    apk add --no-cache bash openjdk8-jre libreoffice  mc && \
    ln -s /usr/bin/python3 /usr/bin/python && \
        cd /usr/lib/libreoffice/share && \
        rm -rf wizards xslt gallery template autocorr basic config emojiconfig labels theme_definitions palette autotext Scripts calc filter psprint tipoftheday && \
        cd /usr/lib/libreoffice/program/ && \
        rm -rf classes opengl shell wizards && \
        rm libmysql_jdbclo.so libmysqlclo.so postgresql-sdbc.ini libpostgresql-sdbclo.so libpostgresql-sdbc-impllo.so && \
        rm libsclo.so libsdlo.so libchartcontrollerlo.so libchartcorelo.so libswuilo.so libdict_??.so libdbulo.so libfrmlo.so libdbaselo.so libdbalo.so && \
        rm libdbahsqllo.so libdbpool2.so libdbaxmllo.so liblocaledata_euro.so liblocaledata_others.so libcuilo.so libdeploymentgui.so

ADD content/bin/ /usr/local/bin/
