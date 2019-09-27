#!/bin/bash -e
DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"

cp -f "$DIR/../../script/messaging.py" "$DIR/feeder"
cp -f "$DIR/../../script/zkstate.py" "$DIR/feeder"

echo "Build platform $PLATFORM..."
. "${DIR}/../../script/build.sh"

