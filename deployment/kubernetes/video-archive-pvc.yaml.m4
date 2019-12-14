
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-archive
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: video-archive
  resources:
    requests:
      storage: defn(`VIDEO_ARCHIVE_VOLUME_SIZE')Gi
