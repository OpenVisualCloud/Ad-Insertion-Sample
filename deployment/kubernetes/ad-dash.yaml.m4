
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-dash
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: cache-storage
  resources:
    requests:
      storage: 1Gi

