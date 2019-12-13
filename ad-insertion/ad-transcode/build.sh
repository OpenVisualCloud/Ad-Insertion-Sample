#!/bin/bash -e

IMAGE="ssai_ad_transcode"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
