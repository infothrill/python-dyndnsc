# Get the tag from an external script
TAG := $(shell ./prepare_source.sh)
# DIR points to the directory with the Dockerfile to be built:
BUILD ?= x86-alpine
DIR ?= $(addprefix $(PWD), /$(BUILD))
DOCKER_REPO ?= dyndnsc-$(shell basename $(DIR))
IMAGE_NAME ?= $(DOCKER_REPO):$(TAG)

default: build

build:
	docker build -t $(IMAGE_NAME) -f $(DIR)/Dockerfile .
	# docker tag $(IMAGE_NAME) $(DOCKER_REPO):latest

push:
	docker push $(IMAGE_NAME)
	docker push $(DOCKER_REPO)

test:
	docker run --rm $(IMAGE_NAME) /usr/bin/dyndnsc --help

rmi:
	docker rmi -f $(IMAGE_NAME)

post_checkout:
	# arm builds on docker hub, from https://github.com/docker/hub-feedback/issues/1261
	curl -L https://github.com/balena-io/qemu/releases/download/v5.2.0%2Bbalena4/qemu-5.2.0.balena4-arm.tar.gz | tar zxvf - -C . && mv qemu-5.2.0+balena4-arm/qemu-arm-static .
	docker run --rm --privileged multiarch/qemu-user-static:register --reset

post_push:
	docker tag $(IMAGE_NAME) $(DOCKER_REPO):$(TAG)
	docker push $(DOCKER_REPO):$(TAG)

rebuild: rmi build
