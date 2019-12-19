#!/bin/bash -e

IMAGE="ssai_ad_content_segment"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=$DIR/../../volume/ad:/mnt:rw" "--volume=$DIR:/home:ro")

. "$DIR/../../script/shell.sh"
