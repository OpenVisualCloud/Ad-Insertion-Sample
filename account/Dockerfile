FROM ubuntu:18.04

RUN  DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q python3-tornado && rm -rf /var/lib/apt/lists/*

COPY    *.py /home/
CMD     ["/bin/bash","-c","/home/main.py"]
WORKDIR /home
EXPOSE  80

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home
USER ${USER}
####
