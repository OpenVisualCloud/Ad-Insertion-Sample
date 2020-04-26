# ssai_analytics_gst_xeon

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.4 as build

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq git ca-certificates python3 python3-pip && rm -rf /var/lib/apt/lists/*
ARG VA_SERVING_REPO=https://gitlab.devtools.intel.com/video-analytics/video-analytics-serving.git
ARG VA_SERVING_BRANCH="develop"

RUN  git clone ${VA_SERVING_REPO} -b ${VA_SERVING_BRANCH} --depth 1

RUN pip3 install --ignore-installed --target /home/build -r video-analytics-serving/requirements.txt

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.4

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q python3-gst-1.0 python3-jsonschema python3-pip ca-certificates && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

COPY --from=build /home/build/ /usr/lib/python3/dist-packages
COPY --from=build /home/video-analytics-serving/vaserving /home/vaserving

COPY models/ /home/models/
RUN mv /home/models/object_detection/1/mobilenet-ssd.json.gst /home/models/object_detection/1/mobilenet-ssd.json && \
    mv /home/models/emotion_recognition/1/emotions-recognition-retail-0003.json.gst /home/models/emotion_recognition/1/emotions-recognition-retail-0003.json && \
    mv /home/models/face_detection_adas/1/face-detection-adas-0001.json.gst /home/models/face_detection_adas/1/face-detection-adas-0001.json && \
    mv /home/models/face_detection_retail/1/face-detection-retail-0004.json.gst /home/models/face_detection_retail/1/face-detection-retail-0004.json && \
    mv /home/models/landmarks_regression/1/landmarks-regression-retail-0009.json.gst /home/models/landmarks_regression/1/landmarks-regression-retail-0009.json

COPY gallery/ /home/gallery/
COPY Xeon/gst/pipelines/ /home/pipelines/
COPY *.py /home/
COPY --from=ssai_common /home/*.py /home/
ENV LOG_LEVEL "DEBUG"
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
