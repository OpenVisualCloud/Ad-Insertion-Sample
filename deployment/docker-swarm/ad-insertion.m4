
    ad-insertion-service:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:ro
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:ro
        environment:
            AD_INTERVALS: 12
            AD_DURATION: 10
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

    ad-insertion-service-2:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:ro
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:ro
        environment:
            AD_INTERVALS: 12
            AD_DURATION: 10
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

    ad-insertion-service-3:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:ro
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:ro
        environment:
            AD_INTERVALS: 12
            AD_DURATION: 10
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

    ad-insertion-service-4:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_DASH_VOLUME}:/var/www/adinsert/dash:ro
            - ${AD_HLS_VOLUME}:/var/www/adinsert/hls:ro
        environment:
            AD_INTERVALS: 12
            AD_DURATION: 10
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
