
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-archive
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: archive
  resources:
    requests:
      storage: 1Gi
