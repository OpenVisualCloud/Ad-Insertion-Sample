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
shift
. "$DIR/build.sh"
docker stack deploy -c "$yml" adi
