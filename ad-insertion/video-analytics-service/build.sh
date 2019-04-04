#!/bin/bash -e
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/messaging.py" "$DIR/feeder"
cp -f "$DIR/../../script/zkstate.py" "$DIR/feeder"
. "$DIR/../../script/build.sh"
