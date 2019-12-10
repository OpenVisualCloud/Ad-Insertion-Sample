#!/bin/bash -e

IMAGE="ad_content_service_frontend"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
