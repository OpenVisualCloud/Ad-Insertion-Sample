#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

# delete all pods, services and deployments
for yaml in $(find "${DIR}" -maxdepth 1 \( -name "*.yaml" ! -name "*-storage.yaml" ! -name "*-pvc.yaml" \) -print); do
    echo $yaml
    kubectl delete -f "$yaml" --ignore-not-found=true 2>/dev/null || echo -n ""
done

# delete all pvcs
for yaml in $(find "${DIR}" -maxdepth 1 -name "*-pvc.yaml" -print); do
    kubectl delete -f "$yaml" --ignore-not-found=true 2>/dev/null || echo -n ""
done

# delete pvs and scs
for yaml in $(find "${DIR}" -maxdepth 1 -name "*-storage.yaml" -print); do
    kubectl delete -f "$yaml" --ignore-not-found=true 2>/dev/null || echo -n ""
done

kubectl delete secret self-signed-certificate 2> /dev/null || echo -n ""
