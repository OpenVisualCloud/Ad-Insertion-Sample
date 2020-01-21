
    zookeeper-service:
        image: confluentinc/cp-zookeeper:5.3.1
        environment:
            ZOOKEEPER_SERVER_ID: 1
            ZOOKEEPER_CLIENT_PORT: '2181'
            ZOOKEEPER_TICK_TIME: '2000'
            KAFKA_HEAP_OPTS: '-Xmx20g -Xms20g'
            ZOOKEEPER_MAX_CLIENT_CNXNS: '40000'
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

