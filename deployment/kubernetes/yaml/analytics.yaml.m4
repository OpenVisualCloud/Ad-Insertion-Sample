include(platform.m4)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: analytics
  labels:
     app: analytics
spec:
  replicas: defn(`NANALYTICS')
  selector:
    matchLabels:
      app: analytics
  template:
    metadata:
      labels:
        app: analytics
    spec:
      enableServiceLinks: false
      containers:
        - name: analytics
          image: defn(`REGISTRY_PREFIX')`ssai_analytics_'defn(`FRAMEWORK')`_'defn(`PLATFORM_SUFFIX'):latest
          imagePullPolicy: IfNotPresent
          env:
            - name: `NETWORK_PREFERENCE'
              value: "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            - name: VA_PRE
              value: "defn(`PLATFORM')-"
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
defn(`PLATFORM_VOLUME_MOUNTS')dnl
defn(`PLATFORM_VOLUMES')dnl
PLATFORM_NODE_SELECTOR(`VCAC-A')dnl
