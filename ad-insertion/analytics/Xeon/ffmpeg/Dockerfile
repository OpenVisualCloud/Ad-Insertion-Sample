# ssai_analytics_ffmpeg_xeon

From openvisualcloud/xeon-ubuntu1804-analytics-ffmpeg:20.4 as build

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq git ca-certificates python3 python3-pip && rm -rf /var/lib/apt/lists/*
ARG VA_SERVING_REPO=https://gitlab.devtools.intel.com/video-analytics/video-analytics-serving.git
ARG VA_SERVING_BRANCH="ovc_integration"
ARG VA_SERVING_TAG="a73d641de1f26c4c7b3f3fbcf805b2427347d994"

RUN  git clone ${VA_SERVING_REPO} -b ${VA_SERVING_BRANCH} --depth 1
RUN  cd video-analytics-serving; git checkout ${VA_SERVING_TAG}
RUN pip3 install --ignore-installed --target /home/build -r video-analytics-serving/requirements.txt
RUN rm -rf /home/video-analytics-serving/vaserving/__main__.py
RUN rm -rf /home/video-analytics-serving/vaserving/rest_api

From openvisualcloud/xeon-ubuntu1804-analytics-ffmpeg:20.4

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-gst-1.0 python3-jsonschema python3-pip && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

COPY --from=build /home/build/ /usr/lib/python3/dist-packages
COPY --from=build /home/video-analytics-serving/vaserving /home/vaserving
COPY ./models/ /home/models/
COPY ./gallery/ /home/gallery/
COPY ./Xeon/ffmpeg/pipelines/ /home/pipelines
COPY *.py /home/
COPY --from=ssai_common /home/*.py /home/
ENV FRAMEWORK=ffmpeg
WORKDIR /home
CMD ["/home/main.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home;
USER ${USER}
####
