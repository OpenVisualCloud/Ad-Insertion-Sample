
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-cache
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ad-cache
  resources:
    requests:
      storage: defn(`AD_CACHE_VOLUME_SIZE')Gi

