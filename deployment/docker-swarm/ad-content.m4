
    ad-content-service:
        image: ad_content_service_frontend:latest
        volumes:
            - ${AD_ARCHIVE_VOLUME}:/var/www/archive:ro
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

