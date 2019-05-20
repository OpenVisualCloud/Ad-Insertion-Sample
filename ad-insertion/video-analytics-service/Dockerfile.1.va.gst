# video_analytics_service_gstreamer
ARG base_name=xeon-ubuntu1804-dldt-gst-va

FROM ${base_name}:build AS gst-python-build

ARG FRAMEWORK=gstreamer

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python-gi-dev \
    git \
    autoconf \
    automake \
    libtool \
    gobject-introspection \
    curl\
    inetutils-ping\
    libsoup2.4.1\
    && rm -rf /var/lib/apt/lists/*; fi

RUN git clone https://gitlab.freedesktop.org/gstreamer/gst-python.git \
    && cd gst-python \
    && git checkout 1.14.4 \
    && ./autogen.sh --prefix=/usr --libdir=/usr/lib/x86_64-linux-gnu --libexecdir=/usr/lib/x86_64-linux-gnu --enable-introspection -- \
        --with-pygi-overrides-dir=/usr/lib/python3/dist-packages/gi/overrides \
        --disable-dependency-tracking \
        --disable-silent-rules \
        --with-libpython-dir="/usr/lib/x86_64-linux-gnu/" \
        PYTHON=/usr/bin/python3 \
    && make \
    && make install \
    && make install DESTDIR=/home/build_gst_python; fi


FROM ${base_name}

# Fetch python3 and Install python3
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends libgirepository-1.0-1 libsoup2.4.1 python3-gi python3-kafka python3-kazoo python3-requests python3-tornado python3-pip python3-setuptools python3-wheel &&  \
    rm -rf /var/lib/apt/lists/*;

COPY --from=gst-python-build /home/build_gst_python /
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

ENTRYPOINT ["./docker-entrypoint.sh"]


####
ARG  USER
ARG  GROUP
ARG  UID
ARG  GID
## must use ; here to ignore user exist status code
RUN  groupadd -f -g ${GID} ${GROUP};useradd -d /home -g ${GROUP} -K UID_MAX=${UID} -K UID_MIN=${UID} ${USER};chown -R ${USER}.${GROUP} /home; 
USER ${USER}
####
