
    ad-transcode:
        image: ssai_ad_transcode:latest
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:rw
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:rw
            - ${AD_STATIC_VOLUME}:/var/www/skipped:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

