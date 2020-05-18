include(platform.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ad-transcode
  labels:
     app: ad-transcode
spec:
  replicas: defn(`NTRANSCODES')
  selector:
    matchLabels:
      app: ad-transcode
  template:
    metadata:
      labels:
        app: ad-transcode
    spec:
      enableServiceLinks: false
      securityContext:
        runAsUser: defn(`USERID')
        runAsGroup: defn(`GROUPID')
        fsGroup: defn(`GROUPID')
      containers:
        - name: ad-transcode
          image: defn(`REGISTRY_PREFIX')ssai_ad_transcode:latest
          imagePullPolicy: IfNotPresent
          env:
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /var/www/adinsert
              name: ad-cache
            - mountPath: /var/www/adsegment
              name: ad-segment
              readOnly: true
      volumes:
          - name: ad-cache
            persistentVolumeClaim:
               claimName: ad-cache
          - name: ad-segment
            persistentVolumeClaim:
               claimName: ad-segment
PLATFORM_NODE_SELECTOR(`Xeon')dnl
