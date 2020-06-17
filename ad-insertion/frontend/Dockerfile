
FROM ssai_common

COPY   *.py /home/
COPY   *.conf /etc/nginx/
CMD    ["/bin/bash","-c","/home/main.py&/usr/sbin/nginx"]
WORKDIR /home
EXPOSE 8080

####
ARG  USER=docker
ARG  GROUP=docker
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  [ ${GID} -gt 0 ] && groupadd -f -g ${GID} ${GROUP}; \
     [ ${UID} -gt 0 ] && useradd -d /home -g ${GID} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER}; \
     touch /var/run/nginx.pid && \
     mkdir -p /var/log/nginx /var/lib/nginx /var/www/cache /var/www/adstatic /var/www/adinsert && \
     chown -R ${UID}:${GID} /home /var/run/nginx.pid /var/www /var/log/nginx /var/lib/nginx
USER ${UID}
####

