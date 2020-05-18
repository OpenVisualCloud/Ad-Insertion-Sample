#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

rm -rf "$DIR/../../volume/ad/cache"
mkdir -p "$DIR/../../volume/ad/cache/dash" "$DIR/../../volume/ad/cache/hls"
mkdir -p "$DIR/../../volume/ad/segment/dash" "$DIR/../../volume/ad/segment/hls"
mkdir -p "$DIR/../../volume/video/cache/dash" "$DIR/../../volume/video/cache/hls"

if [ -x /usr/bin/kubectl ] || [ -x /usr/local/bin/kubectl ]; then
    # list all workers
    hosts=($(kubectl get node -l vcac-zone!=yes -o custom-columns=NAME:metadata.name,STATUS:status.conditions[-1].type,TAINT:spec.taints | grep " Ready " | grep -v "NoSchedule" | cut -f1 -d' '))
    if test ${#hosts[@]} -eq 0; then
        printf "\nFailed to locate worker node(s) for shared storage\n\n"
        exit 1
    elif test ${#hosts[@]} -lt 2; then
        hosts=(${hosts[0]} ${hosts[0]})
    fi

    echo "Generating persistent volume scripts"
    . "$DIR/volume-info.sh" "${hosts[@]}"
    find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
    for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
        m4 $(env | grep _VOLUME_ | sed 's/^/-D/') "${template}" > "${template/.m4/}"
    done
fi
