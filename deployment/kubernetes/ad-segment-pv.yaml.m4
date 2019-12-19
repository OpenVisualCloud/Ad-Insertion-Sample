
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ad-segment
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: ad-segment
spec:
  capacity:
    storage: defn(`AD_SEGMENT_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ad-segment
  local:
    path: defn(`AD_SEGMENT_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`AD_SEGMENT_VOLUME_HOST')"

