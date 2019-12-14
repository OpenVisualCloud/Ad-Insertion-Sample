#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
export AD_ARCHIVE_VOLUME=$(readlink -f "$DIR/../../volume/ad/archive")
export AD_DASH_VOLUME=$(readlink -f "$DIR/../../volume/ad/cache/dash")
export AD_HLS_VOLUME=$(readlink -f "$DIR/../../volume/ad/cache/hls")
export AD_STATIC_VOLUME=$(readlink -f "$DIR/../../volume/ad/static")
export VIDEO_ARCHIVE_VOLUME=$(readlink -f "$DIR/../../volume/video/archive")
export VIDEO_DASH_VOLUME=$(readlink -f "$DIR/../../volume/video/cache/dash")
export VIDEO_HLS_VOLUME=$(readlink -f "$DIR/../../volume/video/cache/hls")

docker container prune -f
docker volume prune -f
docker network prune -f

rm -rf "${AD_DASH_VOLUME}" "${AD_HLS_VOLUME}"
mkdir -p "${AD_DASH_VOLUME}" "${AD_HLS_VOLUME}"

yml="$DIR/docker-compose.$(hostname).yml"
test -f "$yml" || yml="$DIR/docker-compose.yml"

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
case "$1" in
docker_compose)
    dcv="$(docker-compose --version | cut -f3 -d' ' | cut -f1 -d',')"
    mdcv="$(printf '%s\n' $dcv 1.20 | sort -r -V | head -n 1)"
    if test "$mdcv" = "1.20"; then
        echo ""
        echo "docker-compose >=1.20 is required."
        echo "Please upgrade docker-compose at https://docs.docker.com/compose/install."
        echo ""
        exit 0
    fi

    "$DIR/../certificate/self-sign.sh"
    shift
    . "$DIR/build.sh"
    docker-compose -f "$yml" -p adi --compatibility up
    ;;
*)
    "$DIR/../certificate/self-sign.sh"
    shift
    . "$DIR/build.sh"
    docker stack deploy -c "$yml" adi
    ;;
esac
