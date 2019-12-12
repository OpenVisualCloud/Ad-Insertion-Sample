
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-hls
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  storageClassName: cache

