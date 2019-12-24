
    ad-insertion-service:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:ro
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:ro
        environment:
            AD_INTERVALS: 8
            AD_DURATION: 5
            AD_BENCH_MODE: 0
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

