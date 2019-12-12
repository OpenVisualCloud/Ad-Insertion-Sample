
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-dash
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  storageClassName: cache

