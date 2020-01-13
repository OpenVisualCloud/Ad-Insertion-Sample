# ssai_analytics_gst_xeon

FROM openvisualcloud/xeon-ubuntu1804-analytics-gst:20.1

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q python3-gst-1.0 python3-jsonschema python3-pip ca-certificates && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

COPY app /home/
COPY models/ /home/models/
COPY gallery/ /home/gallery/
COPY Xeon/gst/pipelines/ /home/pipelines/
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
