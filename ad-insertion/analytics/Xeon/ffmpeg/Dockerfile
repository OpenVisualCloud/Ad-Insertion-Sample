# ssai_analytics_ffmpeg_xeon

FROM centos:7.6.1810 as build

ARG  VA_SERVING_REPO=https://raw.githubusercontent.com/intel/video-analytics-serving
ARG  VA_SERVING_TAG="v0.3.0-alpha"

RUN  mkdir -p /home/vaserving/common/utils && touch /home/vaserving/__init__.py /home/vaserving/common/__init__.py /home/vaserving/common/utils/__init__.py && for x in common/utils/logging.py common/settings.py arguments.py ffmpeg_pipeline.py gstreamer_pipeline.py model_manager.py pipeline.py pipeline_manager.py schema.py vaserving.py; do curl -o /home/vaserving/$x -L ${VA_SERVING_REPO}/${VA_SERVING_TAG}/vaserving/$x; done

COPY ./models/ /home/models/
COPY ./gallery/ /home/gallery/
COPY ./Xeon/ffmpeg/pipelines/ /home/pipelines
COPY *.py /home/
COPY --from=ssai_common /home/*.py /home/

From openvisualcloud/xeon-ubuntu1804-analytics-ffmpeg:20.7

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-gst-1.0 python3-jsonschema python3-pip && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

COPY --from=build /home/ /home/
ENV FRAMEWORK=ffmpeg
WORKDIR /home
CMD ["/home/analyze.py"]

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     chown -R ${UID}:${GID} /home
USER ${UID}
####
