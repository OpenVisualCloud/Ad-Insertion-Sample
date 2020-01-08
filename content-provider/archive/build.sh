#!/bin/bash -e

IMAGE="ssai_content_provider_archive"
DIR=$(dirname $(readlink -f "$0"))
sample_video="https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master"
clips=("$sample_video/bottle-detection.mp4" "$sample_video/one-by-one-person-detection.mp4" "$sample_video/car-detection.mp4" "$sample_video/people-detection.mp4")

case "$(cat /proc/1/sched | head -n 1)" in
*build.sh*)
    cd /mnt
    mkdir -p archive cache/dash cache/hls
    for clip in "${clips[@]}"; do
        clip_name="${clip/*\//}"
        clip_name="${clip_name/*=/}"
        clip_name="${clip_name/.mp4/}.mp4"
        if test ! -f "archive/$clip_name"; then
            case "$clip" in
                *youtube*)
                    youtube-dl -f 'mp4[width=2160]/mp4[width=1440]/mp4[width=1080]/mp4[width=720]/mp4[width=640]/mp4[width=480]' -o "archive/$clip_name" "$clip"
                    ;;
                *)
                    wget -O "archive/$clip_name" "$clip"
                    ;;
            esac
        fi
    done
    for clip in `find archive -name "*.mp4" -print`; do
        clip_name="${clip/*\//}"
        if test ! -f "archive/$clip_name".png; then
            ffmpeg -i "archive/$clip_name" -vf "thumbnail,scale=640:360" -frames:v 1 -y "archive/$clip_name".png
        fi
        if test -z "`ffprobe -i archive/$clip_name -show_streams -select_streams a -loglevel error | grep STREAM`"; then
            ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 -i "archive/$clip_name" -shortest -c:v copy -c:a aac -y "archive/tmp.$clip_name"
            mv -f "archive/tmp.$clip_name" "archive/$clip_name"
        fi
        if test "$1" == "dash"; then
            /home/create_dash.sh "$clip_name" ${2}&
        fi
        if test "$1" == "hls"; then
            /home/create_hls.sh "$clip_name" ${2}&
        fi
    done
    wait
    ;;
*) 
    mkdir -p "$DIR/../../volume/video/archive"
    mkdir -p "$DIR/../../volume/video/cache/dash"
    mkdir -p "$DIR/../../volume/video/cache/hls"
    . "$DIR/../../script/build.sh"
    . "$DIR/shell.sh" /home/build.sh $@
    ;;
esac
