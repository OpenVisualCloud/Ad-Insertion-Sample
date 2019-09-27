#!/bin/bash -e

IMAGE="ssai_self_certificate"
DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"

. "$DIR/../../script/build.sh"

if test -f "${DIR}/docker-compose.yml.m4"; then
    echo "Generating docker-compose.yml with PLATFORM=${PLATFORM}"
    m4 -DPLATFORM=${PLATFORM} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
fi

