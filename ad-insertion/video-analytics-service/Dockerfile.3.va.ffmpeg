# video_analytics_service_ffmpeg

From xeon-ubuntu1804-dldt-ffmpeg-va

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends libgirepository-1.0-1 libsoup2.4.1 python3-gi python3-kafka python3-kazoo python3-requests python3-tornado python3-pip python3-setuptools python3-wheel &&  \
    rm -rf /var/lib/apt/lists/*;
    
COPY --from=models_base /home/video-analytics/models/ /home/video-analytics/models/ 
COPY ./app/server/requirements.txt /
RUN pip3 install  --no-cache-dir -r /requirements.txt
COPY ./samples /home/video-analytics/samples
COPY ./app /home/video-analytics/app
COPY ./models/ /home/video-analytics/models/
COPY ./pipelines /home/video-analytics/pipelines
COPY  ./feeder/*.py /home/video-analytics/feeder/
COPY   docker-entrypoint.sh /home/video-analytics/

WORKDIR /home/video-analytics

ENTRYPOINT ["./docker-entrypoint.sh", "--framework", "ffmpeg" , "--pipeline_dir", "pipelines/ffmpeg"]

####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home; 
USER ${USER}
####
