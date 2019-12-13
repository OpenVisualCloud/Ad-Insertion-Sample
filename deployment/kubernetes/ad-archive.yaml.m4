
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-archive
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  storageClassName: archive
