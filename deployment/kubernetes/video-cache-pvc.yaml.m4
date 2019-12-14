
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: video-cache
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: cache-storage
  resources:
    requests:
      storage: defn(`VIDEO_CACHE_VOLUME_SIZE')Gi
