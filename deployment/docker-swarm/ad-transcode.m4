
    ad-transcode:
        image: ssai_ad_transcode:latest
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:rw
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:rw
            - ${AD_SEGMENT_DASH_VOLUME}:/var/www/adinsert/segment/dash:ro
            - ${AD_SEGMENT_HLS_VOLUME}:/var/www/adinsert/segment/hls:ro
            - ${AD_STATIC_VOLUME}:/var/www/skipped:ro
        networks:
            - appnet
        deploy:
            replicas: 8
            placement:
                constraints:
                    - node.role==manager

