
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-archive
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  storageClassName: archive

