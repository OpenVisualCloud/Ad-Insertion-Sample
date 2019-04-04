#!/bin/bash -e

IMAGE="ssai_content_provider_frontend"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/messaging.py" "$DIR"
. "$DIR/../../script/build.sh"
