
    ad-insertion-service:
        image: defn(`REGISTRY_PREFIX')ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_CACHE_VOLUME}:/var/www/adinsert:ro
            - ${AD_STATIC_VOLUME}:/var/www/adstatic:ro
            - /etc/localtime:/etc/localtime:ro
        environment:
            AD_INTERVALS: 8
            AD_DURATION: 5
            AD_SEGMENT: 5
            AD_BACKOFF: 3
            AD_BENCH_MODE: 0
            AD_ANALYTIC_AHEAD: 3
            AD_TRANSCODE_AHEAD: 2
            EVERY_NTH_FRAME: 6
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes
