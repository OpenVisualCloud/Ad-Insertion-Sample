#!/bin/bash -e

IMAGE="ad_content_service_frontend"
DIR=$(dirname $(readlink -f "$0"))

cp -f "${DIR}/../../script/messaging.py" "${DIR}"
. "$DIR/../../script/build.sh"
