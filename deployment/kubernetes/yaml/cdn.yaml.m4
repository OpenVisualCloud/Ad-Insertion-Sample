include(platform.m4)

apiVersion: v1
kind: Service
metadata:
  name: cdn-service
  labels:
    app: cdn
spec:
  ports:
    - port: 443
      targetPort: 8443
      name: https
  externalIPs:
    - defn(`HOSTIP')
  selector:
    app: cdn

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cdn
  labels:
     app: cdn
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cdn
  template:
    metadata:
      labels:
        app: cdn
    spec:
      enableServiceLinks: false
      containers:
        - name: cdn
          image: defn(`REGISTRY_PREFIX')ssai_cdn_service:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8443
          env:
            - name: NO_PROXY
              value: "*"
            - name: no_proxy
              value: "*"
          volumeMounts:
            - mountPath: /etc/localtime
              name: timezone
              readOnly: true
            - mountPath: /var/run/secrets
              name: self-signed-certificate
              readOnly: true
      volumes:
        - name: timezone
          hostPath:
            path: /etc/localtime
            type: File
        - name: self-signed-certificate
          secret:
            secretName: self-signed-certificate
PLATFORM_NODE_SELECTOR(`Xeon')dnl
