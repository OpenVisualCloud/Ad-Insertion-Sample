
    ad-insertion-service:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:ro
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:ro
        depends_on:
            - content-provider
            - kafka-service
            - zookeeper
        environment:
            AD_INTERVALS: 8
            AD_DURATION: 5
            AD_BENCH_MODE: 0
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: defn(`NINSERTIONS')
            placement:
                constraints:
                    - node.role==manager

