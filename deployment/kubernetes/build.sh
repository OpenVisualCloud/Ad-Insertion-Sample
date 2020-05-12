#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
FRAMEWORK="${2:-gst}"
NANALYTICS="${3:-1}"
NTRANSCODES="${4:-1}"
MINRESOLUTION="${5:-360p}"

rm -rf "$DIR/../../volume/ad/cache"
mkdir -p "$DIR/../../volume/ad/cache/dash" "$DIR/../../volume/ad/cache/hls"
mkdir -p "$DIR/../../volume/ad/segment/dash" "$DIR/../../volume/ad/segment/hls"
mkdir -p "$DIR/../../volume/video/cache/dash" "$DIR/../../volume/video/cache/hls"

if [ -x /usr/bin/kubectl ] || [ -x /usr/local/bin/kubectl ]; then
    HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')
    if [ -z "$HOSTIP" ]; then
        exit 0
    fi

    # list all workers
    hosts=($(kubectl get node -l vcac-zone!=yes -o custom-columns=NAME:metadata.name,STATUS:status.conditions[-1].type,TAINT:spec.taints | grep " Ready " | grep -v "NoSchedule" | cut -f1 -d' '))
    if test ${#hosts[@]} -eq 0; then
        printf "\nFailed to locate worker node(s) for shared storage\n\n"
        exit -1
    elif test ${#hosts[@]} -lt 2; then
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

    echo "Generating templates with PLATFORM=${PLATFORM},FRAMEWORK=${FRAMEWORK},NANALYTICS=${NANALYTICS},NTRANSCODES=${NTRANSCODES},MINRESOLUTION=${MINRESOLUTION}"
    find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
    for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
        yaml=${template/.m4/}
        m4 -DPLATFORM=${PLATFORM} -DFRAMEWORK=${FRAMEWORK} -DNANALYTICS=${NANALYTICS} -DNTRANSCODES=${NTRANSCODES} -DMINRESOLUTION=${MINRESOLUTION} $(env | grep _VOLUME_ | sed 's/^/-D/') -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -I "${DIR}" "${template}" > "${yaml}"
    done
fi
