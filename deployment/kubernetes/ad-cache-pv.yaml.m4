
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ad-cache
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: ad-cache
spec:
  capacity:
    storage: defn(`AD_CACHE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: ad-cache
  local:
    path: defn(`AD_CACHE_VOLUME_PATH')
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`AD_CACHE_VOLUME_HOST')"

