#!/bin/bash -e

DOCKER_REPO=${DOCKER_REPO="https://raw.githubusercontent.com/OpenVisualCloud/Dockerfiles/v1.0/Xeon/ubuntu-18.04"}

DIR=$(dirname $(readlink -f "$0"))

curl ${DOCKER_REPO}/ffmpeg/Dockerfile > "$DIR/Dockerfile"
