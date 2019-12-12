
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-dash
spec:
  accessModes:
    - ReadWriteMany
  volumeMode: Filesystem
  storageClassName: cache

