
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-segment
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: ad-segment
  resources:
    requests:
      storage: defn(`AD_SEGMENT_VOLUME_SIZE')Gi

