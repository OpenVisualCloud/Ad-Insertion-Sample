#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
case "$1" in 
    ffmpeg)
        IMAGE="video_analytics_service_ffmpeg"
        DOCKERFILE="$DIR/Dockerfile.3"
        ;;
    gstreamer)
        IMAGE="video_analytics_service_gstreamer"
        DOCKERFILE="$DIR/Dockerfile.1"
        ;;
    *)
        echo "Usage: ffmpeg|gstreamer"
        exit 3
        ;;
esac

shift    #first argument is parsed
OPTIONS[0]="--rm"
OPTIONS[1]="--name=${IMAGE}"
. "$DIR/../../script/shell.sh"
