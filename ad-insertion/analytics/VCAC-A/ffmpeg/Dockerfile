# ssai_analytics_ffmpeg_vcac-a

ARG base_name=openvisualcloud/vcaca-ubuntu1804-analytics-ffmpeg:20.4

FROM ${base_name} as build

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && apt-get install -qq git ca-certificates python3 python3-pip && rm -rf /var/lib/apt/lists/*
ARG VA_SERVING_REPO=https://gitlab.devtools.intel.com/video-analytics/video-analytics-serving.git
ARG VA_SERVING_BRANCH="develop"

RUN  git clone ${VA_SERVING_REPO} -b ${VA_SERVING_BRANCH} --depth 1

RUN pip3 install --ignore-installed --target /home/build -r video-analytics-serving/requirements.txt

FROM ${base_name}
 
# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends libgirepository-1.0-1 libsoup2.4.1 libjson-c3 python3-jsonschema python3-gi python3-requests python3-tornado python3-pip python3-setuptools python3-wheel && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'
    
COPY --from=build /home/build/ /usr/lib/python3/dist-packages
COPY --from=build /home/video-analytics-serving/vaserving /home/vaserving
COPY models/ /home/models/
COPY gallery/ /home/gallery/
COPY VCAC-A/ffmpeg/pipelines/ /home/pipelines/
COPY *.py /home/
COPY --from=ssai_common /home/*.py /home/

WORKDIR /home
CMD ["/home/main.py"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home; 
#USER ${USER}
####
