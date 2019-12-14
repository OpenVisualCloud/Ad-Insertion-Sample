
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-static
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ad-static-storage
  resources:
    requests:
      storage: defn(`AD_STATIC_VOLUME_SIZE')Gi
