
    kafka2db:
        image: defn(`REGISTRY_PREFIX')ssai_kafka2db:latest
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

