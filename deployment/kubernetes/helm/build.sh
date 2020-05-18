#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
FRAMEWORK="${2:-gst}"
NANALYTICS="${3:-1}"
NTRANSCODES="${4:-1}"
MINRESOLUTION="${5:-360p}"
NETWORK="${6:-FP32}"
REGISTRY="$7"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

echo "Generating helm chart"
. "$DIR/../volume-info.sh"
m4 -DREGISTRY_PREFIX=${REGISTRY} -DPLATFORM=${PLATFORM} -DFRAMEWORK=${FRAMEWORK} -DNANALYTICS=${NANALYTICS} -DNTRANSCODES=${NTRANSCODES} -DMINRESOLUTION=${MINRESOLUTION} -DNETWORK_PREFERENCE=${NETWORK} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} $(env | grep _VOLUME_ | sed 's/^/-D/') -I "${DIR}/adi" "$DIR/adi/values.yaml.m4" > "$DIR/adi/values.yaml"
