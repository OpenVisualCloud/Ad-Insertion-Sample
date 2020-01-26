    kafka-service:
        image: wurstmeister/kafka:2.12-2.4.0
        environment:
            KAFKA_BROKER_ID: 1
            KAFKA_ZOOKEEPER_CONNECT: zookeeper-service:2181
            KAFKA_LISTENERS: PLAINTEXT://:9092
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-service:9092
            KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
            KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
            KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
            KAFKA_DEFAULT_REPLICATION_FACTOR: 1
            KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
            KAFKA_NUM_PARTITIONS: 8
            KAFKA_LOG_RETENTION_MINUTES: 30
            KAFKA_HEAP_OPTS: '`-Xmx'ifelse(defn(`PLATFORM'),`Xeon',2,16)g `-Xms'ifelse(defn(`PLATFORM'),`Xeon',2,16)g'
            KAFKA_LOG4J_ROOT_LOGLEVEL: 'ERROR'
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

