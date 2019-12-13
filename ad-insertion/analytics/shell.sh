#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM=${1:-Xeon}
shift
FRAMEWORK=${1:-gst}
shift

IMAGE="ssai_analytics_${FRAMEWORK}_$(echo ${PLATFORM} | tr A-Z a-z)"
OPTIONS=("--rm" "--name=${IMAGE}")
. "$DIR/../../script/shell.sh"
