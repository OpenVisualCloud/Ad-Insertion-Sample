
    ad-insertion-service:
        image: ssai_ad_insertion_frontend:latest
        volumes:
            - ${AD_CACHE_VOLUME}:/var/www/adinsert:ro
            - ${AD_STATIC_VOLUME}:/var/www/adstatic:ro
            - /etc/localtime:/etc/localtime:ro
        environment:
            AD_INTERVALS: 12
            AD_DURATION: 10
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
            replicas: ifelse(defn(`PLATFORM'),`Xeon',1,1)
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes
