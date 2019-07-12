#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
XEON_DIR=$DIR/platforms/Xeon
VCAC_A_DIR=$DIR/platforms/VCAC-A

# ffmpeg base dockerfile
DOCKER_REPO="https://raw.githubusercontent.com/OpenVisualCloud/Dockerfiles/v1.2/Xeon/ubuntu-18.04/analytics/ffmpeg"

base_name=xeon-ubuntu1804-dldt-ffmpeg-va
docker_file="$XEON_DIR/Dockerfile.4.ffmpeg.xeon"

echo "# "${base_name} > ${docker_file}
curl ${DOCKER_REPO}/Dockerfile >> ${docker_file}

# gst base dockerfile
DOCKER_REPO="https://raw.githubusercontent.com/OpenVisualCloud/Dockerfiles/v1.2/Xeon/ubuntu-18.04/analytics/gst"

base_name=xeon-ubuntu1804-dldt-gst-va
docker_file="$XEON_DIR/Dockerfile.2.gst.xeon"

echo "# "${base_name} > ${docker_file}
curl ${DOCKER_REPO}/Dockerfile>> ${docker_file}

# gst base dockerfile vcac-a
DOCKER_REPO="https://raw.githubusercontent.com/fkhoshne/Dockerfiles/vcaca/VCAC-A/ubuntu-16.04/analytics/gst"

base_name=vcac-a-ubuntu1604-openvino-gst-va
docker_file="$VCAC_A_DIR/Dockerfile.2.gst.vcac-a"

echo "# "${base_name} > ${docker_file}
curl ${DOCKER_REPO}/Dockerfile>> ${docker_file}

# ffmpeg base dockerfile vcaa
DOCKER_REPO="https://raw.githubusercontent.com/fkhoshne/Dockerfiles/vcaca/VCAC-A/ubuntu-16.04/analytics/ffmpeg"

base_name=vcac-a-ubuntu1604-openvino-ffmpeg-va
docker_file="$VCAC_A_DIR/Dockerfile.4.ffmpeg.vcac-a"

echo "# "${base_name} > ${docker_file}
curl ${DOCKER_REPO}/Dockerfile >> ${docker_file}

