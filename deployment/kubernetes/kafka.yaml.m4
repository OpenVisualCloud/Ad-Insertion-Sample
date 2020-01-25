
apiVersion: v1
kind: Service
metadata:
  name: kafka-service
  labels:
    app: kafka
spec:
  ports:
  - port: 9092
    protocol: TCP
  selector:
    app: kafka

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka
  labels:
    app: kafka
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
    spec:
      enableServiceLinks: false
      containers:
        - name: kafka
          image: confluentinc/cp-kafka:5.4.0
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9092
          env:
            - name: "KAFKA_BROKER_ID"
              value: "1"
            - name: "KAFKA_ZOOKEEPER_CONNECT"
              value: "zookeeper-service:2181"
            - name: "KAFKA_ADVERTISED_LISTENERS"
              value: "PLAINTEXT://kafka-service:9092,PLAINTEXT_HOST://localhost:29092"
            - name: "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP"
              value: "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT"
            - name: "KAFKA_INTER_BROKER_LISTENER_NAME"
              value: "PLAINTEXT"
            - name: "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR"
              value: "1"
            - name: "KAFKA_DEFAULT_REPLICATION_FACTOR"
              value: "1"
            - name: "KAFKA_AUTO_CREATE_TOPICS_ENABLE"
              value: "false"
            - name: "KAFKA_NUM_PARTITIONS"
              value: "16"
            - name: "KAFKA_LOG_RETENTION_MINUTES"
              value: "30"
            - name: "KAFKA_CONNECTIONS_MAX_IDLE_MS"
              value: "10800000"
            - name: "KAFKA_HEAP_OPTS"
              value: "-Xmx1024m -Xms1024m"
            - name: "KAFKA_LOG4J_LOGGERS"
              value: "kafka=ERROR,kafka.controller=ERROR,state.change.logger=ERROR,org.apache.kafka=ERROR"
            - name: "KAFKA_LOG4J_ROOT_LOGLEVEL"
              value: "ERROR"
            - name: "CONFLUENT_SUPPORT_METRICS_ENABLE"
              value: "0"

---

apiVersion: batch/v1
kind: Job
metadata:
  name: kafka-init
spec:
  template:
    spec:
      enableServiceLinks: false
      containers:
        - name: kafka-init
          image: confluentinc/cp-kafka:5.4.0
          imagePullPolicy: IfNotPresent
          command: ["/bin/bash","-c","cub kafka-ready -b kafka-service:9092 1 20 && \
  kafka-topics --create --topic content_provider_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
  kafka-topics --create --topic seg_analytics_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
  kafka-topics --create --topic seg_analytics_data --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
  kafka-topics --create --topic ad_transcode_sched --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
  kafka-topics --create --topic workloads --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181 && \
  kafka-topics --create --topic adstats --partitions 16 --replication-factor 1 --if-not-exists --zookeeper zookeeper-service:2181"]
          env:
            - name: "KAFKA_BROKER_ID"
              value: "ignored"
            - name: "KAFKA_ZOOKEEPER_CONNECT"
              value: "ignored"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
      restartPolicy: Never
