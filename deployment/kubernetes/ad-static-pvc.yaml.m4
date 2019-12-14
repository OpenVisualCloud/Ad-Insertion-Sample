
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-static
spec:
  accessModes:
    - ReadOnlyMany
  storageClassName: ad-static
  resources:
    requests:
      storage: defn(`AD_STATIC_VOLUME_SIZE')Gi
