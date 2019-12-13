
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cache-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: ad-dash
spec:
  capacity:
    storage: defn(`AD_CACHE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: cache-storage
  local:
    path: defn(`AD_CACHE_VOLUME_PATH')/dash
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`AD_CACHE_VOLUME_HOST')"

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: ad-hls
spec:
  capacity:
    storage: defn(`AD_CACHE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: cache-storage
  local:
    path: defn(`AD_CACHE_VOLUME_PATH')/hls
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`AD_CACHE_VOLUME_HOST')"

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: video-dash
spec:
  capacity:
    storage: defn(`VIDEO_CACHE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: cache-storage
  local:
    path: defn(`VIDEO_CACHE_VOLUME_PATH')/dash
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`VIDEO_CACHE_VOLUME_HOST')"

---

apiVersion: v1
kind: PersistentVolume
metadata:
  name: video-hls
spec:
  capacity:
    storage: defn(`VIDEO_CACHE_VOLUME_SIZE')Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: cache-storage
  local:
    path: defn(`VIDEO_CACHE_VOLUME_PATH')/hls
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - "defn(`VIDEO_CACHE_VOLUME_HOST')"

