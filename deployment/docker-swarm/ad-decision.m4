
    ad-decision-service:
        image: defn(`REGISTRY_PREFIX')ssai_ad_decision_frontend:latest
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes

