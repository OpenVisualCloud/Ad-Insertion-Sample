#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

echo "Making volumes..."
awk -v DIR="$DIR" '
/name:/ {
    gsub("-","/",$2)
    content="\""DIR"/../../volume/"$2"\""
}
/path:/ {
    path=$2
}
/- ".*"/ {
    host=substr($2,2,length($2)-2);
    paths[host][path]=1;
    contents[host][path]=content
}
END {
    for (host in paths) {
        for (path in paths[host]) {
            system("ssh "host" \"mkdir -p "path";find "path" -mindepth 1 -maxdepth 1 -exec rm -rf {} \\\\;\"");
            system("scp -r "contents[host][path]"/* "host":"path);
        }
    }
}
' "$DIR"/*-storage.yaml
