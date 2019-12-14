
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ad-archive
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: ad-archive
spec:
  capacity:
    storage: defn(`AD_ARCHIVE_VOLUME_SIZE')Gi
  accessModes:
  - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ad-archive
  local:
    path: defn(`AD_ARCHIVE_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`AD_ARCHIVE_VOLUME_HOST')"

