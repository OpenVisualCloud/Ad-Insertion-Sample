#!/bin/bash -e

IMAGE="ad_decision_service"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
