#!/bin/bash -e

PLATFORM=$(echo $1 | tr A-Z a-z)
IMAGE="ssai_ad_content_frontend_$PLATFORM"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/inventory.json.$PLATFORM" "$DIR/inventory.json";;
. "$DIR/../../script/build.sh"
