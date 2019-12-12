
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-hls
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  storageClassName: cache

