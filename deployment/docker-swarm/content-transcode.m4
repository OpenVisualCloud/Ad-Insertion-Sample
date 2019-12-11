
    content-transcode:
        image: ssai_content_provider_transcode:latest
        volumes:
            - ${VIDEO_ARCHIVE_VOLUME}:/var/www/archive:ro
            - ${VIDEO_DASH_VOLUME}:/var/www/dash:rw
            - ${VIDEO_HLS_VOLUME}:/var/www/hls:rw
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: 2
            placement:
                constraints:
                    - node.role==manager
