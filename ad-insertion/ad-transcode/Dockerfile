
FROM xeon-ubuntu1804-ffmpeg

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends python3-kafka python3-kazoo python3-requests; \
    rm -rf /var/lib/apt/lists/*;

COPY   *.py /home/
CMD    ["/bin/bash","-c","/home/main.py"]
WORKDIR /home

####
#ARG  USER
#ARG  GROUP
#ARG  UID
#ARG  GID
## must use ; here to ignore user exist status code
#RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home; \
#     mkdir -p /var/www/adinsert/dash /var/www/adinsert/hls /var/www/skipped && \
#     chown -R ${USER}.${GROUP} /var/www /var/www/adinsert/dash /var/www/adinsert/hls /var/www/skipped
#VOLUME ["/var/www/adinsert/dash","/var/www/adinsert/hls","/var/www/skipped"]
#USER ${USER}
####

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/cache && \
     chown -R ${USER}.${GROUP} /var/run/nginx.pid /var/www /var/log/nginx /var/lib/nginx
USER ${USER}
####

