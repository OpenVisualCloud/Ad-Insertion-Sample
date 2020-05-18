include(platform.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-transcode
  labels:
     app: content-transcode
spec:
  replicas: defn(`NTRANSCODES')
  selector:
    matchLabels:
      app: content-transcode
  template:
    metadata:
      labels:
        app: content-transcode
    spec:
      enableServiceLinks: false
      securityContext:
        runAsUser: defn(`USERID')
        runAsGroup: defn(`GROUPID')
        fsGroup: defn(`GROUPID')
      containers:
        - name: content-transcode
          image: defn(`REGISTRY_PREFIX')ssai_content_transcode:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /var/www/video
              name: video-cache
            - mountPath: /var/www/archive
              name: video-archive
              readOnly: true
      volumes:
          - name: video-cache
            persistentVolumeClaim:
               claimName: video-cache
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
PLATFORM_NODE_SELECTOR(`Xeon')dnl
