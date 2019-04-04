#!/bin/bash -e

IMAGE="ssai_cdn_service"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../script/db.py" "$DIR"
cp -f "$DIR/../script/messaging.py" "$DIR"
. "$DIR/../script/build.sh"
