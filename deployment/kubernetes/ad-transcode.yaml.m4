
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ad-transcode
  labels:
     app: ad-transcode
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ad-transcode
  template:
    metadata:
      labels:
        app: ad-transcode
    spec:
      enableServiceLinks: false
      containers:
        - name: ad-transcode
          image: ssai_ad_transcode:latest
          imagePullPolicy: IfNotPresent
          volumeMounts:
            - mountPath: /var/www/adinsert/dash
              name: ad-dash
            - mountPath: /var/www/adinsert/hls
              name: ad-hls
            - mountPath: /var/www/skipped
              name: ad-static
              readOnly: true
      volumes:
          - name: ad-dash
            persistentVolumeClaim:
               claimName: ad-dash
          - name: ad-hls
            persistentVolumeClaim:
               claimName: ad-hls
          - name: ad-static
            persistentVolumeClaim:
               claimName: ad-static
