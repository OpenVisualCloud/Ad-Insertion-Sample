
FROM openvisualcloud/xeon-ubuntu1804-media-ffmpeg:20.7

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends nginx python3-tornado python3-urllib3 python3-requests python3-psutil python3-pip && rm -rf /var/lib/apt/lists/* && \
    pip3 install 'kafka-python>=1.4.7' 'kazoo>=2.6.1'

COPY --from=ssai_common /home/*.py /home/
COPY   *.py /home/
CMD    ["/bin/bash","-c","/home/main.py"]
WORKDIR /home

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/cache && \
     chown -R ${UID}:${GID} /home /var/run/nginx.pid /var/www /var/log/nginx /var/lib/nginx
USER ${UID}
####

