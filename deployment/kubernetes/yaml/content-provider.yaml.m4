include(platform.m4)

apiVersion: v1
kind: Service
metadata:
  name: content-provider-service
  labels:
    app: content-provider
spec:
  ports:
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
          image: defn(`REGISTRY_PREFIX')ssai_content_provider_frontend:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          ports:
            - containerPort: 8080
          volumeMounts:
            - mountPath: /var/www/archive
              name: video-archive
              readOnly: true
            - mountPath: /var/www/video
              name: video-cache
              readOnly: true
      volumes:
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
          - name: video-cache
            persistentVolumeClaim:
               claimName: video-cache
PLATFORM_NODE_SELECTOR(`Xeon')dnl
