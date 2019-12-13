# ssai_analytics_gst_vcaca 

FROM openvisualcloud/vcaca-ubuntu1804-analytics-gst:19.11

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends libjson-c3 python3-gst-1.0 python3-jsonschema python3-gi python3-requests python3-tornado python3-pip python3-setuptools python3-wheel python3-kafka python3-kazoo &&  rm -rf /var/lib/apt/lists/*;

#COPY ./app/server/requirements.txt /

COPY app /home/
COPY models/ /home/models/
COPY gallery/ /home/gallery/
COPY VCAC-A/gst/pipelines/ /home/pipelines/
COPY *.py /home/
COPY --from=ssai_common /home/*.py /home/

WORKDIR /home
CMD ["/home/main.py"]

###
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home;
USER ${USER}
####
#
