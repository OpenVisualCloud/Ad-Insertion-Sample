
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ad-static
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: ad-static
spec:
  capacity:
    storage: defn(`AD_STATIC_VOLUME_SIZE')Gi
  accessModes:
  - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ad-static
  local:
    path: defn(`AD_STATIC_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`AD_STATIC_VOLUME_HOST')"

