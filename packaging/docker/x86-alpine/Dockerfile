# use multi stage dockerfile to first create a virtualenv,
# then copy the virtualenv (without all build deps) into target image

FROM alpine:3.7 as build
RUN apk -U update && apk -U upgrade
RUN apk -U add python3 py3-virtualenv python3-dev gcc musl-dev linux-headers
ADD src /src
RUN virtualenv /usr/local/dyndnsc && \
    /usr/local/dyndnsc/bin/pip install /src

FROM alpine:3.7
RUN apk -U update && \
    apk -U upgrade && \
    apk -U add --no-cache python3 && \
    rm -rf /var/cache/apk/*
COPY --from=build /usr/local/dyndnsc /usr/local/dyndnsc
RUN ln -s /usr/local/dyndnsc/bin/dyndnsc /usr/local/bin/dyndnsc

ENTRYPOINT ["/usr/local/bin/dyndnsc"]
