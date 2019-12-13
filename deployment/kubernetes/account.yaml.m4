
apiVersion: v1
kind: Service
metadata:
  name: account-service
  labels:
    app: account
spec:
  - port: 8080
    protocol: TCP
  selector:
    app: account

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: account
  labels:
     app: account
spec:
  replicas: 1
  selector:
    matchLabels:
      app: account
  template:
    metadata:
      labels:
        app: account
    spec:
      enableServiceLinks: false
      containers:
        - name: account
          image: ssai_account_service:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
