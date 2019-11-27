#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
YML="$DIR/../deployment/docker-swarm/docker-compose.yml"

mkdir -p "$DIR/../archive"
for image in `grep 'image:' "$YML" | awk '{print$2}'` ssai_content_provider_archive:latest ssai_self_certificate:latest ssai_ad_insertion_ad_static:latest ssai_ad_content_archive:latest; do
    imagefile=${image//\//-}
    imagefile=${imagefile//:/-}
    echo "archiving $image => $imagefile"
    (docker image save "$image" > "$DIR/../archive/${imagefile}.tar") || (docker pull "$image" && (docker image save "$image" > "$DIR/../archive/${imagefile}.tar"))
done
