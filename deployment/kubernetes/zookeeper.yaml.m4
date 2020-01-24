
apiVersion: v1
kind: Service
metadata:
  name: zookeeper-service
  labels:
    app: zookeeper
spec:
  ports:
  - port: 2181
    protocol: TCP
  selector:
    app: zookeeper

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: zookeeper
  labels:
     app: zookeeper
spec:
  replicas: 1
  selector:
    matchLabels:
      app: zookeeper
  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      enableServiceLinks: false
      containers:
        - name: zookeeper
          image: confluentinc/cp-zookeeper:5.3.1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 2181
          env:
            - name: "ZOOKEEPER_SERVER_ID"
              value: "1"
            - name: "ZOOKEEPER_CLIENT_PORT"
              value: "2181"
            - name: "ZOOKEEPER_TICK_TIME"
              value: "3600000"
            - name: "ZOOKEEPER_HEAP_OPTS"
              value: "-Xmx1024m -Xms1024m"
            - name: "ZOOKEEPER_MAX_CLIENT_CNXNS"
              value: "20000"
            - name: "ZOOKEEPER_SESSION_TIMEOUT_MS"
              value: "7200000"
            - name: "ZOOKEEPER_LOG4J_LOGGERS"
              value: "zookeepr=ERROR"
            - name: "ZOOKEEPER_LOG4J_ROOT_LOGLEVEL"
              value: "ERROR"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
