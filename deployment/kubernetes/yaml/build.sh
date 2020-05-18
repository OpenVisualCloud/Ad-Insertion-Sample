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

echo "Generating templates with PLATFORM=${PLATFORM},FRAMEWORK=${FRAMEWORK},NANALYTICS=${NANALYTICS},NTRANSCODES=${NTRANSCODES},MINRESOLUTION=${MINRESOLUTION},NETWORK=${NETWORK}"
. "$DIR/../volume-info.sh"
find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    yaml=${template/.m4/}
    m4 -DREGISTRY_PREFIX=${REGISTRY} -DPLATFORM=${PLATFORM} -DFRAMEWORK=${FRAMEWORK} -DNANALYTICS=${NANALYTICS} -DNTRANSCODES=${NTRANSCODES} -DMINRESOLUTION=${MINRESOLUTION} -DNETWORK_PREFERENCE=${NETWORK} $(env | grep _VOLUME_ | sed 's/^/-D/') -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -I "${DIR}" "${template}" > "${yaml}"
done
