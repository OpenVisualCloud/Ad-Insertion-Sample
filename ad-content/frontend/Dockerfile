FROM ubuntu:18.04

RUN apt-get update && apt-get install -y -q --no-install-recommends nginx python3-tornado python3-kafka;

COPY    *.py /home/
COPY    inventory.json /home/
COPY    *.conf /etc/nginx/
CMD    ["/bin/bash","-c","/home/main.py&/usr/sbin/nginx"]
VOLUME ["/var/www/archive"]
WORKDIR /home
EXPOSE  8080

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

