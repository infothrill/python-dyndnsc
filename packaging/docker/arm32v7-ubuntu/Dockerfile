# use multi stage dockerfile to first create a virtualenv,
# then copy the virtualenv (without all build deps) into target image

FROM ghcr.io/linuxserver/baseimage-ubuntu:arm32v7-focal as build
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-virtualenv python3-dev python3-wheel gcc
COPY qemu-arm-static /usr/bin
ADD src /src
RUN virtualenv /usr/local/dyndnsc && \
    /usr/local/dyndnsc/bin/pip install /src

FROM ghcr.io/linuxserver/baseimage-ubuntu:arm32v7-focal
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 && \
    rm -rf /var/cache/apt/*
COPY --from=build /usr/local/dyndnsc /usr/local/dyndnsc
RUN ln -s /usr/local/dyndnsc/bin/dyndnsc /usr/local/bin/dyndnsc

ENTRYPOINT ["/usr/local/bin/dyndnsc"]
