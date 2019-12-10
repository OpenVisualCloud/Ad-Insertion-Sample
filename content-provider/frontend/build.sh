#!/bin/bash -e

IMAGE="ssai_content_provider_frontend"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
