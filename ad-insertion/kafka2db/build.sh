#!/bin/bash -e

IMAGE="ssai_analytic_db"
DIR=$(dirname $(readlink -f "$0"))

. "$DIR/../../script/build.sh"
