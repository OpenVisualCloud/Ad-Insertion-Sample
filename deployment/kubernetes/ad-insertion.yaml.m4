
apiVersion: v1
kind: Service
metadata:
  name: ad-insertion-service
  labels:
    app: ad-insertion
spec:
  - port: 8080
    protocol: TCP
  selector:
    app: ad-insertion

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ad-insertion
  labels:
     app: ad-insertion
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ad-insertion
  template:
    metadata:
      labels:
        app: ad-insertion
    spec:
      enableServiceLinks: false
      containers:
        - name: ad-insertion
          image: ssai_ad_insertion_frontend:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          env:
            - name: AD_INTERVALS
              value: 8
            - name: AD_DURATION
              value: 5
            - name: AD_BENCH_MODE
              value: 0
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /var/www/adinsert/dash
              name: ad-dash
              readOnly: true
            - mountPath: /var/www/adinsert/hls
              name: ad-hls
              readOnly: true
      volumes:
          - name: ad-dash
            persistentVolumeClaim:
               claimName: ad-dash
          - name: ad-hls
            persistentVolumeClaim:
               claimName: ad-hls
