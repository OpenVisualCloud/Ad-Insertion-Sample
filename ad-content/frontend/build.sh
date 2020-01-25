#!/bin/bash -e

IMAGE="ssai_ad_content_frontend"
DIR=$(dirname $(readlink -f "$0"))

case "$1" in 
    Xeon)
        cp -f inventory.json.all inventory.json;;
    VCAC-A)
        cp -f inventory.json.obj inventory.json;;
esac

. "$DIR/../../script/build.sh"
