
FROM xeon-ubuntu1804-ffmpeg

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q python3-kafka python3-kazoo python3-psutil && rm -rf /var/lib/apt/lists/*

COPY   *.py /home/
CMD    ["/bin/bash","-c","/home/workload.py tx&/home/main.py"]
VOLUME ["/var/www/archive","/var/www/dash","/var/www/hls"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home
USER ${USER}
####
