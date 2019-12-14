#!/bin/bash -e

IMAGE="ssai_ad_insertion_frontend"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=${DIR}/../../volume/ad/cache/dash:/var/www/adinsert/dash:ro" "--volume=${DIR}/../../volume/ad/cache/hls:/var/www/adinsert/hls:ro" "--volume=${DIR}/../../volume/ad/static:/var/www/skipped:ro")

. "$DIR/../../script/shell.sh"
