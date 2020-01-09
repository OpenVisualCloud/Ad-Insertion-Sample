# ssai_analytics_ffmpeg_xeon

From openvisualcloud/xeon-ubuntu1804-analytics-ffmpeg:19.11

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-gst-1.0 python3-jsonschema python3-pip && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'
    
COPY app /home/
COPY ./models/ /home/models/
COPY ./gallery/ /home/gallery/
COPY ./Xeon/ffmpeg/pipelines/ /home/pipelines
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
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home; 
USER ${USER}
####
