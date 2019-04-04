#!/bin/bash -e

IMAGE="ssai_ad_insertion_ad_static"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=$DIR/../../volume/ad/static:/mnt:rw" "--volume=$DIR:/home:ro")

. "$DIR/../../script/shell.sh"
