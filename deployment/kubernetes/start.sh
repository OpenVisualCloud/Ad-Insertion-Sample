#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

for yaml in $(find "$DIR" -maxdepth 1 -name "*.yaml" -print); do
    kubectl apply -f "$yaml"
done
