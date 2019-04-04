#!/bin/bash -e

IMAGE="ssai_account_service"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../script/build.sh"
