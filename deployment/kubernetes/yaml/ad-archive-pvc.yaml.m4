
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ad-archive
spec:
  accessModes:
    - ReadOnlyMany
  storageClassName: ad-archive
  resources:
    requests:
      storage: defn(`AD_ARCHIVE_VOLUME_SIZE')Gi

