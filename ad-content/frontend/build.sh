#!/bin/bash -e

IMAGE="ssai_ad_content_frontend"
DIR=$(dirname $(readlink -f "$0"))

case "$1" in 
    Xeon)
        cp -f "$DIR/inventory.json.all" "$DIR/inventory.json";;
    VCAC-A)
        cp -f "$DIR/inventory.json.obj" "$DIR/inventory.json";;
esac

. "$DIR/../../script/build.sh"
