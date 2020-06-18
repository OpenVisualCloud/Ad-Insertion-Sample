include(platform.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka2db
  labels:
     app: kafka2db
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka2db
  template:
    metadata:
      labels:
        app: kafka2db
    spec:
      enableServiceLinks: false
      containers:
        - name: kafka2db
          image: defn(`REGISTRY_PREFIX')ssai_kafka2db:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
PLATFORM_NODE_SELECTOR(`Xeon')dnl
