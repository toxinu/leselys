FROM prologic/python-runtime

EXPOSE 5000

VOLUME /data

ENTRYPOINT ["/entrypoint.sh"]
CMD []

RUN apk -U add build-base && \
	apk -U add libxml2-dev && \
	apk -U add libxslt-dev && \
	apk -U add git && \
    rm -rf /var/cache/apk/*

WORKDIR /app
COPY . /app/
RUN pip install .

COPY dockerfiles/entrypoint.sh /entrypoint.sh

WORKDIR /data
