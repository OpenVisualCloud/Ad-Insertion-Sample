
    content-transcode:
        image: ssai_content_transcode:latest
        volumes:
            - ${VIDEO_ARCHIVE_VOLUME}:/var/www/archive:ro
            - ${VIDEO_DASH_VOLUME}:/var/www/video/dash:rw
            - ${VIDEO_HLS_VOLUME}:/var/www/video/hls:rw
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: defn(`NTRANSCODES')
            placement:
                constraints:
                    - node.role==manager
