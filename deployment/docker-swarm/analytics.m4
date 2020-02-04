
ifelse(defn(`PLATFORM'),`Xeon',`dnl
    analytics:
        image: `ssai_analytics_'defn(`FRAMEWORK')_xeon:latest
        environment:
            NETWORK_PREFERENCE: "{\"CPU\":\"INT8,FP32\"}"
            VA_PRE: "defn(`PLATFORM')-"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes
')dnl

ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
    analytics:
        image: vcac-container-launcher:latest
        environment:
            VCAC_IMAGE: `ssai_analytics_'defn(`FRAMEWORK')_vcac-a:latest
            VCAC_VA_PRE: "VCAC-A-"
            VCAC_NO_PROXY: "*"
            VCAC_no_proxy: "*"
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
            - /etc/localtime:/etc/localtime:ro
        networks:
            - appnet 
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - node.labels.vcac_zone==yes
')dnl

