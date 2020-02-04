#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

yml="$DIR/docker-compose.$(hostname).yml"
test -f "$yml" || yml="$DIR/docker-compose.yml"

docker stack services adi
echo "Shutting down stack adi..."
while test -z "$(docker stack rm adi 2>&1 | grep 'Nothing found in stack')"; do
    sleep 2
done

docker container prune -f
docker volume prune -f
docker network prune -f
