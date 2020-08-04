
    zookeeper-service:
        image: zookeeper:3.5.6
        environment:
            ZOO_TICK_TIME: '10000'
            ZOO_MAX_CLIENT_CNXNS: '160000'
            ZOO_AUTOPURGE_PURGEINTERVAL: '1'
            ZOO_LOG4J_PROP: 'ERROR'
        networks:
            - appnet
        user: zookeeper
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes

