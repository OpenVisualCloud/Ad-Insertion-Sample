
    content-provider-service:
        image: ssai_content_provider_frontend:latest
        volumes:
            - ${VIDEO_ARCHIVE_VOLUME}:/var/www/archive:ro
            - ${VIDEO_DASH_VOLUME}:/var/www/video/dash:ro
            - ${VIDEO_HLS_VOLUME}:/var/www/video/hls:ro
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

