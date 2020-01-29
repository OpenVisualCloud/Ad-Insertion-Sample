
    ad-insertion-service:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_CACHE_VOLUME}:/var/www/adinsert:ro
            - ${AD_STATIC_VOLUME}:/var/www/adstatic:ro
        environment:
            AD_INTERVALS: 8
            AD_DURATION: 5
            AD_SEGMENT: 5
            AD_BACKOFF: 3
            AD_BENCH_MODE: 0
            EVERY_NTH_FRAME: 3
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

