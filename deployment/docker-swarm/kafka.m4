
    kafka-service:
        image: confluentinc/cp-kafka:5.3.1
        environment:
            KAFKA_BROKER_ID: 1
            KAFKA_ZOOKEEPER_CONNECT: zookeeper-service:2181
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka-service:9092,PLAINTEXT_HOST://localhost:29092
            KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
            KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
            KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
            KAFKA_DEFAULT_REPLICATION_FACTOR: 1
            KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'false'
            KAFKA_NUM_PARTITIONS: 8
            KAFKA_LOG_RETENTION_MINUTES: 30
            KAFKA_CONNECTIONS_MAX_IDLE_MS: 10800000
            KAFKA_HEAP_OPTS: '`-Xmx'ifelse(defn(`PLATFORM'),`Xeon',2,16)g `-Xms'ifelse(defn(`PLATFORM'),`Xeon',2,16)g'
            KAFKA_LOG4J_LOGGERS: 'kafka=ERROR,kafka.controller=ERROR,state.change.logger=ERROR,org.apache.kafka=ERROR'
            KAFKA_LOG4J_ROOT_LOGLEVEL: 'ERROR'
            CONFLUENT_SUPPORT_METRICS_ENABLE: 0
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

    kafka-init:
        image: confluentinc/cp-kafka:5.3.1
        command: |
              bash -c 'cub kafka-ready -b kafka-service:9092 1 20 && \
                       kafka-topics --create --topic content_provider_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic seg_analytics_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic seg_analytics_data --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic ad_transcode_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic workloads --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic adstats --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
                       kafka-topics --create --topic video_analytics_fps --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181'
        environment:
            KAFKA_BROKER_ID: ignored
            KAFKA_ZOOKEEPER_CONNECT: ignored
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            restart_policy:
                condition: none
            placement:
                constraints:
                    - node.role==manager
