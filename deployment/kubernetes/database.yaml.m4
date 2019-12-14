
apiVersion: v1
kind: Service
metadata:
  name: database-service
  labels:
    app: database
spec:
  ports:
  - port: 9200
    protocol: TCP
  selector:
    app: database

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
  labels:
     app: database
spec:
  replicas: 1
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      enableServiceLinks: false
      containers:
        - name: database
          image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9200
          env:
            - name: "discovery.type"
              value: "single-node"
