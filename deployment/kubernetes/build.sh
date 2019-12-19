#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
FRAMEWORK="${2:-gst}"
NANALYTICS="${3:-1}"
NTRANSCODES="${4:-1}"

rm -rf "$DIR/../../volume/ad/cache"
mkdir -p "$DIR/../../volume/ad/cache/dash" "$DIR/../../volume/ad/cache/hls"
mkdir -p "$DIR/../../volume/ad/segment/dash" "$DIR/../../volume/ad/segment/hls"
mkdir -p "$DIR/../../volume/video/cache/dash" "$DIR/../../volume/video/cache/hls"

if [ -x /usr/bin/kubectl ] || [ -x /usr/local/bin/kubectl ]; then
    HOSTIP=$(kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}' --selector='node-role.kubernetes.io/master' | cut -f1 -d' ')

    # list all workers
    hosts=($(kubectl get nodes -o jsonpath="{.items[*].metadata.name}" --selector='!node-role.kubernetes.io/master'))
    if test ${#hosts[@]} -lt 2; then
        hosts=(${hosts[0]} ${hosts[0]})
    fi

    export AD_ARCHIVE_VOLUME_PATH=/tmp/archive/ad
    export AD_ARCHIVE_VOLUME_SIZE=1
    export AD_ARCHIVE_VOLUME_HOST=${hosts[0]}

    export AD_CACHE_VOLUME_PATH=/tmp/cache/ad
    export AD_CACHE_VOLUME_SIZE=1
    export AD_CACHE_VOLUME_HOST=${hosts[0]}

    export AD_SEGMENT_VOLUME_PATH=/tmp/segment/ad
    export AD_SEGMENT_VOLUME_SIZE=1
    export AD_SEGMENT_VOLUME_HOST=${hosts[0]}

    export AD_STATIC_VOLUME_PATH=/tmp/static/ad
    export AD_STATIC_VOLUME_SIZE=1
    export AD_STATIC_VOLUME_HOST=${hosts[0]}

    export VIDEO_ARCHIVE_VOLUME_PATH=/tmp/archive/video
    export VIDEO_ARCHIVE_VOLUME_SIZE=2
    export VIDEO_ARCHIVE_VOLUME_HOST=${hosts[1]}

    export VIDEO_CACHE_VOLUME_PATH=/tmp/cache/video
    export VIDEO_CACHE_VOLUME_SIZE=2
    export VIDEO_CACHE_VOLUME_HOST=${hosts[1]}

    echo "Generating templates with PLATFORM=${PLATFORM}, FRAMEWORK=${FRAMEWORK}"
    find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
    for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
        yaml=${template/.m4/}
        m4 -DPLATFORM=${PLATFORM} -DFRAMEWORK=${FRAMEWORK} -DNANALYTICS=${NANALYTICS} -DNTRANSCODES=${NTRANSCODES} $(env | grep _VOLUME_ | sed 's/^/-D/') -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -I "${DIR}" "${template}" > "${yaml}"
    done
fi
