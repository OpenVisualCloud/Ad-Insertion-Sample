
apiVersion: v1
kind: Service
metadata:
  name: content-provider-service
  labels:
    app: content-provider
spec:
  - port: 8080
    protocol: TCP
  selector:
    app: content-provider

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-provider
  labels:
     app: content-provider
spec:
  replicas: 1
  selector:
    matchLabels:
      app: content-provider
  template:
    metadata:
      labels:
        app: content-provider
    spec:
      enableServiceLinks: false
      containers:
        - name: content-provider
          image: ssai_content_provider_frontend:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          volumeMounts:
            - mountPath: /var/www/archive
              name: video-archive
              readOnly: true
            - mountPath: /var/www/dash
              name: video-dash
              readOnly: true
            - mountPath: /var/www/hls
              name: video-dash
              readOnly: true
      volumes:
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
          - name: video-dash
            persistentVolumeClaim:
               claimName: video-dash
          - name: video-hls
            persistentVolumeClaim:
               claimName: video-hls
