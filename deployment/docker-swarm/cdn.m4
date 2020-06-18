
    cdn-service:
        image: defn(`REGISTRY_PREFIX')ssai_cdn_service:latest
        ports:
            - "ifelse(defn(`PLATFORM'),`Xeon',8443,443):8443"
            - "ifelse(defn(`PLATFORM'),`Xeon',8080,80):8080"
        environment:
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager
                    - node.labels.vcac_zone!=yes
        secrets:
            - source: self_crt
              target: /var/run/secrets/self.crt
              uid: ${USER_ID}
              gid: ${GROUP_ID}
              mode: 0444
            - source: self_key
              target: /var/run/secrets/self.key
              uid: ${USER_ID}
              gid: ${GROUP_ID}
              mode: 0440

