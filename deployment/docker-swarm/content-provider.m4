
    content-provider-service:
        image: ssai_content_provider_frontend:latest
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - ${VIDEO_ARCHIVE_VOLUME}:/var/www/archive:ro
            - ${VIDEO_DASH_VOLUME}:/var/www/video/dash:ro
            - ${VIDEO_HLS_VOLUME}:/var/www/video/hls:ro
        networks:
            - appnet
        deploy:
            replicas: ifelse(defn(`PLATFORM'),`Xeon',1,2)
            placement:
                constraints:
                    - node.role==manager
