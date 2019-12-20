#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
clips=()

case "$(cat /proc/1/sched | head -n 1)" in
*build.sh*)
    cd /mnt
    for clip in "${clips[@]}"; do
        clip_name="${clip/*=/}.mp4"
        if test ! -f "$clip_name"; then
            youtube-dl -f 'mp4[width=1920]/mp4[width=1280]/mp4[width=640]/mp4[width=480]' -o "$clip_name" "$clip"
        fi
    done
    ;;
*) 
    download="false"
    mkdir -p "${DIR}/../../volume/ad/archive"
    for clip in "${clips[@]}"; do
        if test ! -f "${DIR}/../../volume/ad/archive/${clip/*=/}.mp4"; then
            download="true"
        fi
    done

    IMAGE="ssai_ad_content_archive"
    . "$DIR/../../script/build.sh"
    if test "$download" = "true"; then
        . "$DIR/shell.sh" /home/build.sh
    fi
    ;;
esac
