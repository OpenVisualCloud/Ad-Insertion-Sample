
apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-transcode
  labels:
     app: content-transcode
spec:
  replicas: 1
  selector:
    matchLabels:
      app: content-transcode
  template:
    metadata:
      labels:
        app: content-transcode
    spec:
      enableServiceLinks: false
      containers:
        - name: content-transcode
          image: ssai_content_transcode:latest
          imagePullPolicy: IfNotPresent
          volumeMounts:
            - mountPath: /var/www/dash
              name: video-dash
            - mountPath: /var/www/hls
              name: video-hls
            - mountPath: /var/www/archive
              name: video-archive
              readOnly: true
      volumes:
          - name: video-dash
            persistentVolumeClaim:
               claimName: video-dash
          - name: video-hls
            persistentVolumeClaim:
               claimName: video-hls
          - name: video-archive
            persistentVolumeClaim:
               claimName: video-archive
