
    ad-transcode:
        image: defn(`REGISTRY_PREFIX')ssai_ad_transcode:latest
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - ${AD_CACHE_VOLUME}:/var/www/adinsert:rw
            - ${AD_SEGMENT_VOLUME}:/var/www/adsegment:ro
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet
        deploy:
            replicas: defn(`NTRANSCODES')
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes
