
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: archive-storage
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
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: archive-storage
  local:
    path: defn(`AD_ARCHIVE_VOLUME_PATH')
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`AD_ARCHIVE_VOLUME_HOST')"

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: video-archive
spec:
  capacity:
    storage: defn(`VIDEO_ARCHIVE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: archive-storage
  local:
    path: defn(`VIDEO_ARCHIVE_VOLUME_PATH')
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`VIDEO_ARCHIVE_VOLUME_HOST')"

