
    ad-content-service:
        image: defn(`REGISTRY_PREFIX')ssai_ad_content_frontend:latest
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - ${AD_ARCHIVE_VOLUME}:/var/www/archive:ro
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes

