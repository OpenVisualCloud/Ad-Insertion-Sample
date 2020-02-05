#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

yml="$DIR/docker-compose.$(hostname).yml"
test -f "$yml" || yml="$DIR/docker-compose.yml"
case "$2" in
VCAC-A) 
    name="adia";;
Xeon)
    name="adix";;
esac

docker stack services $name 
echo "Shutting down stack $name..."
while test -z "$(docker stack rm $name 2>&1 | grep 'Nothing found in stack')"; do
    sleep 2
done

docker container prune -f
docker volume prune -f
docker network prune -f
