# ssai_analytics_gst_vcac-a

FROM centos:7.6.1810 as build

ARG  VA_SERVING_REPO=https://raw.githubusercontent.com/intel/video-analytics-serving
ARG  VA_SERVING_TAG="v0.3.0-alpha"

RUN  mkdir -p /home/vaserving/common/utils && touch /home/vaserving/__init__.py /home/vaserving/common/__init__.py /home/vaserving/common/utils/__init__.py && for x in common/utils/logging.py common/settings.py arguments.py ffmpeg_pipeline.py gstreamer_pipeline.py model_manager.py pipeline.py pipeline_manager.py schema.py vaserving.py; do curl -o /home/vaserving/$x -L ${VA_SERVING_REPO}/${VA_SERVING_TAG}/vaserving/$x; done

COPY models/ /home/models/
RUN mv /home/models/object_detection/1/mobilenet-ssd.json.gst /home/models/object_detection/1/mobilenet-ssd.json && \
    mv /home/models/emotion_recognition/1/emotions-recognition-retail-0003.json.gst /home/models/emotion_recognition/1/emotions-recognition-retail-0003.json && \
    mv /home/models/face_detection_adas/1/face-detection-adas-0001.json.gst /home/models/face_detection_adas/1/face-detection-adas-0001.json && \
    mv /home/models/face_detection_retail/1/face-detection-retail-0004.json.gst /home/models/face_detection_retail/1/face-detection-retail-0004.json && \
    mv /home/models/landmarks_regression/1/landmarks-regression-retail-0009.json.gst /home/models/landmarks_regression/1/landmarks-regression-retail-0009.json && \
    mv /home/models/face_reidentification/1/face-reidentification-retail-0095.json.gst /home/models/face_reidentification/1/face-reidentification-retail-0095.json

COPY gallery/ /home/gallery/
RUN mv /home/gallery/face_gallery_FP16/gallery.json.gst /home/gallery/face_gallery_FP16/gallery.json && \
    mv /home/gallery/face_gallery_FP32/gallery.json.gst /home/gallery/face_gallery_FP32/gallery.json

COPY VCAC-A/gst/pipelines/ /home/pipelines/
COPY *.py /home/
COPY --from=ssai_common /home/*.py /home/

FROM openvisualcloud/vcaca-ubuntu1804-analytics-gst:20.7
# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends libjson-c3 python3-gst-1.0 python3-jsonschema python3-gi python3-requests python3-tornado python3-pip python3-setuptools python3-wheel libjemalloc-dev &&  rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

# libjemalloc used by va-serving to avoid memory growth
ENV LD_PRELOAD=libjemalloc.so

COPY --from=build /home/ /home/
ENV FRAMEWORK gstreamer
WORKDIR /home
CMD ["/home/analyze.py"]

###
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
