#!/bin/bash -e

case "$0" in
    *restore*)
        for tarfile in dist/*.tar; do
            docker load -i "$tarfile"
        done
        tar xvfzm dist/dirs.tgz
        ;;
    *)
        DIR=$(dirname $(readlink -f "$0"))
        YML="$DIR/../deployment/docker-swarm/docker-compose.yml"
        rm -rf "$DIR/../dist"
        if test -e "$YML"; then
            mkdir -p "$DIR/../dist/dist"
            for image in `awk -v 'labels=*' -f "$DIR/scan-yaml.awk" "$YML"` ssai_content_provider_archive:latest ssai_self_certificate:latest ssai_ad_insertion_ad_static:latest ssai_ad_content_archive:latest; do
                imagefile=${image//\//-}
                imagefile=${imagefile//:/-}
                echo "archiving $image => $imagefile"
                (docker image save "$image" > "$DIR/../dist/dist/${imagefile}.tar") || (docker pull "$image" && (docker image save "$image" > "$DIR/../dist/dist/${imagefile}.tar"))
            done
            (cd "$DIR/.."; tar cfz "$DIR/../dist/dist/dirs.tgz" script deployment doc CMakeLists.txt README.md volume --exclude=doc/asset)
            cp "$0" "$DIR/../dist/restore.sh"
            cp "$DIR/../LICENSE" "$DIR/../dist"
        else
            echo "Missing $YML"
            echo "Sample not fully built? (Please run 'make')"
        fi
        ;;
esac
