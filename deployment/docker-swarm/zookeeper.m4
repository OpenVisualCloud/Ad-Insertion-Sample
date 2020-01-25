
    zookeeper-service:
        image: zookeeper:3.5.6
        environment:
            ZOO_TICK_TIME: '3600000'
            ZOO_MAX_CLIENT_CNXNS: '160000'
            ZOO_AUTOPURGE_PURGEINTERVAL: '8'
            ZOO_SESSION_TIMEOUT_MS: '7200000'
            ZOO_LOG4J_PROP: 'ERROR'
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

