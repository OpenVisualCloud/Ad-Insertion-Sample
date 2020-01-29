# vcaca-ubuntu1804-analytics-gst

FROM openvisualcloud/vcaca-ubuntu1804-dev:20.1 as build
ENV InferenceEngine_DIR=/opt/intel/openvino/deployment_tools/inference_engine/share
RUN apt-get update && apt-get install -y -q git cmake wget uuid-dev automake autotools-dev libtool-bin libssl-dev

ARG VA_GSTREAMER_PLUGINS_REPO=https://github.com/cgdougla/gst-video-analytics
ARG VA_GSTREAMER_PLUGINS_VER=c63804016401f9a102499306ccc8b10e885dff82
RUN git clone ${VA_GSTREAMER_PLUGINS_REPO} && \
    cd gst-video-analytics && \
    git checkout ${VA_GSTREAMER_PLUGINS_VER} && \
    git submodule init && git submodule update && \
    mkdir build && \
    cd build && \
    export CFLAGS="-std=gnu99 -Wno-missing-field-initializers" && \
    export CXXFLAGS="-std=c++11 -Wno-missing-field-initializers" && \
    cmake \
    -DVERSION_PATCH=$(echo "$(git rev-list --count --first-parent HEAD)") \
    -DGIT_INFO=$(echo "git_$(git rev-parse --short HEAD)") \
    -DCMAKE_BUILD_TYPE=Release \
    -DDISABLE_SAMPLES=ON \
    -DHAVE_VAAPI=ON \
    -DENABLE_PAHO_INSTALLATION=1 \
    -DENABLE_RDKAFKA_INSTALLATION=1 \
    -DENABLE_AVX2=ON -DENABLE_SSE42=ON \
    -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr .. && \
    make -j4 && \
    make install

RUN mkdir -p /usr/local/lib/x86_64-linux-gnu/gstreamer-1.0 && cp gst-video-analytics/build/intel64/Release/lib/* /usr/local/lib/x86_64-linux-gnu/gstreamer-1.0

FROM openvisualcloud/vcaca-ubuntu1804-analytics-gst:20.1

COPY --from=build /usr/local/lib/x86_64-linux-gnu/gstreamer-1.0 /usr/local/lib/x86_64-linux-gnu/gstreamer-1.0