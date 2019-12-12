#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
PLATFORM="${1:-Xeon}"
FRAMEWORK="${2:-gst}"
NANALYTICS="${3:-1}"
NINSERTIONS="${4:-1}"
HOSTIP=$(kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}' --selector='node-role.kubernetes.io/master' | cut -f1 -d' ')

echo "Generating templates with PLATFORM=${PLATFORM}, FRAMEWORK=${FRAMEWORK}"
find "${DIR}" -maxdepth 1 -name "*.yaml" -exec rm -rf "{}" \;
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    yaml=${template/.m4/}
    m4 -DPLATFORM=${PLATFORM} -DFRAMEWORK=${FRAMEWORK} -DNANALYTICS=${NANALYTICS} -DNINSERTIONS=${NINSERTIONS} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} -I "${DIR}" "${template}" > "${yaml}"
done
