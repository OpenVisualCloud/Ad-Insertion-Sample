
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
          image: ssai_kafka2db:latest
          imagePullPolicy: IfNotPresent
