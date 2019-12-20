#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
FRAMEWORK="${2:-gst}"
NANALYTICS="${3:-1}"
NTRANSCODES="${4:-1}"
MINRESOLUTION="${5:-360p}"

if test -f "${DIR}/docker-compose.yml.m4"; then
    echo "Generating docker-compose.yml with PLATFORM=${PLATFORM},FRAMEWORK=${FRAMEWORK},NANALYTICS=${NANALYTICS},NTRANSCODES=${NTRANSCODES},MINRESOLUTION=${MINRESOLUTION}"
    m4 -DPLATFORM=${PLATFORM} -DFRAMEWORK=${FRAMEWORK} -DNANALYTICS=${NANALYTICS} -DNTRANSCODES=${NTRANSCODES} -DMINRESOLUTION=${MINRESOLUTION} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
fi

