
FROM xeon-ubuntu1804-ffmpeg
RUN apt-get update && apt-get install -y -q youtube-dl bc wget && rm -rf /var/lib/apt/lists/*;

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home
USER ${USER}
####
