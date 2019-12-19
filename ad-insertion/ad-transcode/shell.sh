#!/bin/bash -e

IMAGE="ssai_ad_transcode"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=${DIR}/../../volume/ad/cache/dash:/var/www/adinsert/dash:ro" "--volume=${DIR}/../../volume/ad/cache/hls:/var/www/adinsert/hls:ro" "--volume=${DIR}/../../volume/ad/static:/var/www/skipped:ro" "--volume=${DIR}/../../volume/ad/segment/dash:/var/www/adinsert/segment/dash:ro" "--volume=${DIR}/../../volume/ad/segment/hls:/var/www/adinsert/segment/hls:ro")

. "$DIR/../../script/shell.sh"
