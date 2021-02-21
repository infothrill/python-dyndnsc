# Docker images for `dyndnsc`

## Usage

### x86

	docker pull infothrill/dyndnsc-x86-alpine

### arm

	docker pull infothrill/dyndnsc-arm32v7-ubuntu

### Running

	docker run -v /etc/dyndnsc.ini:/etc/dyndnsc.ini:ro -t dyndnsc-x86-alpine -vv -c /etc/dyndnsc.ini --loop --log-json

For further reference, please consult https://dyndnsc.readthedocs.io/

## Building

The surrounding scripting allows to

* build locally: `make build`
* build armhf image: `BUILD=armhf-alpine make post_checkout build`
* build x86 and armhf on hub.docker.com using hooks
