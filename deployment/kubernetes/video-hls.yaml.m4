
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-hls
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: cache-storage
  resources:
    requests:
      storage: 5Gi
