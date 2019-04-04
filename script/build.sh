#!/bin/bash -e

if test -z "${DIR}"; then 
    echo "This script should not be called directly."
    exit -1
fi 

# build image(s) in order (to satisfy dependencies)
for dep in .8 .7 .6 .5 .4 .3 .2 .1 ''; do
    if test -f "${DIR}/Dockerfile$dep"; then
        image=$(head -n 1 "$DIR/Dockerfile$dep" | grep '# ' | cut -d' ' -f2)
        if test -z "$dep"; then image="$IMAGE"; fi

        if grep -q 'AS build' "${DIR}/Dockerfile$dep"; then
            sudo docker build --network=host --file="${DIR}/Dockerfile$dep" --target build -t "$image:build" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=$(id -un) --build-arg GROUP=$(id -gn) --build-arg UID=$(id -u) --build-arg GID=$(id -g)
        fi

        sudo docker build --network=host --file="${DIR}/Dockerfile$dep" -t "$image:latest" "$DIR" $(env | grep -E '_(proxy|REPO|VER)=' | sed 's/^/--build-arg /') --build-arg USER=$(id -un) --build-arg GROUP=$(id -gn) --build-arg UID=$(id -u) --build-arg GID=$(id -g)
    fi
done
