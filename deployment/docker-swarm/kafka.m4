
    kafka-service:
        image: confluentinc/cp-kafka:latest
        depends_on:
            - zookeeper-service
        environment:
            KAFKA_BROKER_ID: 1
            KAFKA_ZOOKEEPER_CONNECT: zookeeper-service:2181
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-service:9092,PLAINTEXT_HOST://localhost:29092
            KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
            KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
            KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
            KAFKA_DEFAULT_REPLICATION_FACTOR: 1
            KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'false'
            KAFKA_NUM_PARTITIONS: 16
            KAFKA_LOG_RETENTION_HOURS: 8
            KAFKA_HEAP_OPTS: '-Xmx1024m -Xms1024m'
            KAFKA_LOG4J_LOGGERS: 'kafka=ERROR,kafka.controller=ERROR,state.change.logger=ERROR,org.apache.kafka=ERROR'
            KAFKA_LOG4J_ROOT_LOGLEVEL: 'ERROR'
            CONFLUENT_SUPPORT_METRICS_ENABLE: 0
        restart: always
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

    kafka-init:
        image: confluentinc/cp-kafka:latest
        depends_on:
            - kafka-service
        command: |
              bash -c 'cub kafka-ready -b kafka-service:9092 1 20 && \
                       kafka-topics --create --topic content_provider_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic seg_analytics_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic seg_analytics_data --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic ad_transcode_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic workloads --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic adstats --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       sleep infinity'
        environment:
            KAFKA_BROKER_ID: ignored
            KAFKA_ZOOKEEPER_CONNECT: ignored
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            placement:
                constraints:
                    - node.role==manager

