#!/bin/bash -e

IMAGE="ssai_kafka2db"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
