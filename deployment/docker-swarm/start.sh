#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
export AD_ARCHIVE_VOLUME=$(readlink -f "$DIR/../../volume/ad/archive")
export AD_CACHE_VOLUME=$(readlink -f "$DIR/../../volume/ad/cache")
export AD_SEGMENT_VOLUME=$(readlink -f "$DIR/../../volume/ad/segment")
export AD_STATIC_VOLUME=$(readlink -f "$DIR/../../volume/ad/static")
export VIDEO_ARCHIVE_VOLUME=$(readlink -f "$DIR/../../volume/video/archive")
export VIDEO_CACHE_VOLUME=$(readlink -f "$DIR/../../volume/video/cache")

docker container prune -f
docker volume prune -f
docker network prune -f

for mode in dash hls; do
    rm -rf "${AD_CACHE_VOLUME}/$mode"
    mkdir -p "${AD_CACHE_VOLUME}/$mode"
    mkdir -p "${AD_SEGMENT_VOLUME}/$mode"
    mkdir -p "${VIDEO_CACHE_VOLUME}/$mode"
done

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
