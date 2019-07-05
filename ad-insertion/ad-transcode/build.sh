#!/bin/bash -e

IMAGE="ssai_ad_transcode"
DIR=$(dirname $(readlink -f "$0"))

cp -f "$DIR/../../script/zkstate.py" "$DIR"
cp -f "$DIR/../../script/db.py" "$DIR"
cp -f "$DIR/../../script/abr_hls_dash.py" "$DIR"
cp -f "$DIR/../../script/messaging.py" "$DIR"
cp -f "$DIR/../../script/workload.py" "$DIR"
. "$DIR/../../script/build.sh"
