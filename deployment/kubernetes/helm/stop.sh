#!/bin/bash

DIR=$(dirname $(readlink -f "$0"))

helm uninstall adi
kubectl delete secret self-signed-certificate 2> /dev/null || echo -n ""
