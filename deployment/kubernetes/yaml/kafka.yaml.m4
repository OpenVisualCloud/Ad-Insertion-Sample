include(platform.m4)

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
          image: defn(`REGISTRY_PREFIX')ssai_kafka:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9092
          env:
            - name: "KAFKA_BROKER_ID"
              value: "1"
            - name: "KAFKA_ZOOKEEPER_CONNECT"
              value: "zookeeper-service:2181"
            - name: "KAFKA_LISTENERS"
              value: "PLAINTEXT://:9092"
            - name: "KAFKA_ADVERTISED_LISTENERS"
              value: "PLAINTEXT://kafka-service:9092"
            - name: "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP"
              value: "PLAINTEXT:PLAINTEXT"
            - name: "KAFKA_INTER_BROKER_LISTENER_NAME"
              value: "PLAINTEXT"
            - name: "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR"
              value: "1"
            - name: "KAFKA_DEFAULT_REPLICATION_FACTOR"
              value: "1"
            - name: "KAFKA_AUTO_CREATE_TOPICS_ENABLE"
              value: "true"
            - name: "KAFKA_NUM_PARTITIONS"
              value: "8"
            - name: "KAFKA_LOG_RETENTION_MINUTES"
              value: "30"
            - name: "KAFKA_HEAP_OPTS"
              value: "-Xmx1024m -Xms1024m"
            - name: "KAFKA_LOG4J_ROOT_LOGLEVEL"
              value: "ERROR"
          securityContext:
            runAsUser: 1000
PLATFORM_NODE_SELECTOR(`Xeon')dnl
