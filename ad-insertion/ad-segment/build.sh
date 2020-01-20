#!/bin/bash -e

IMAGE="ssai_ad_content_segment"
DIR=$(dirname $(readlink -f "$0"))
clips=()

case "$(cat /proc/1/sched | head -n 1)" in
*build.sh*)
    cd /mnt
    mkdir -p segment/archive segment/dash segment/hls
    for clip in `find archive -name "*.mp4" -print`; do
        clip_name="${clip/*\//}"
        #echo $clip_name
        if test ! -f "segment/archive/$clip_name"; then
            ffmpeg -i "archive/$clip_name" -vf "scale=1920:960,pad=1920:1080:0:60:black,drawtext=text='Server-Side AD Insertion':x=(w-text_w)/2:y=(h-text_h)/3:fontsize=100:fontcolor=white:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf" -y "segment/archive/$clip_name"
        fi
        if test "$1" == "dash"; then
            /home/create_dash.sh "$clip_name" ${2} &
        fi
        if test "$1" == "hls"; then
            /home/create_hls.sh "$clip_name" ${2} &
        fi
    done
    wait
    ;;
*)
    mkdir -p "$DIR/../../volume/ad/archive"
    mkdir -p "$DIR/../../volume/ad/segment/archive"
    mkdir -p "$DIR/../../volume/ad/segment/hls"
    mkdir -p "$DIR/../../volume/ad/segment/dash"
    . "$DIR/../../script/build.sh"
    . "$DIR/shell.sh" /home/build.sh $@
    ;;
esac

