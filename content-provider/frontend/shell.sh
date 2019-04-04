#!/bin/bash -e

IMAGE="ssai_content_provider_frontend"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=${DIR}/../../volume/video/archive:/var/www/archive:ro" "--volume=${DIR}/../../volume/video/dash:/var/www/dash:ro" "--volume=${DIR}/../../volume/video/hls:/var/www/hls:ro")

. "$DIR/../../script/shell.sh"
