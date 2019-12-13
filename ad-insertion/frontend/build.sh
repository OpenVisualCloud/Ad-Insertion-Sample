#!/bin/bash -e

IMAGE="ssai_ad_insertion_frontend"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
