
    zookeeper-service:
        image: confluentinc/cp-zookeeper:5.3.1
        environment:
            ZOOKEEPER_SERVER_ID: 1
            ZOOKEEPER_CLIENT_PORT: '2181'
            ZOOKEEPER_TICK_TIME: '3600000'
            KAFKA_HEAP_OPTS: '-Xmx512m -Xms512m'
            ZOOKEEPER_MAX_CLIENT_CNXNS: '20000'
            ZOOKEEPER_SESSION_TIMEOUT_MS: '7200000'
            ZOOKEEPER_LOG4J_LOGGERS: 'zookeepr=ERROR'
            ZOOKEEPER_LOG4J_ROOT_LOGLEVEL: 'ERROR'
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

