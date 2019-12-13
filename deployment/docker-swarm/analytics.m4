
ifelse(defn(`PLATFORM'),`Xeon',`dnl
    analytics:
        image: `ssai_analytics_'defn(`FRAMEWORK')_xeon:latest
        deploy:
            replicas: defn(`NANALYTICS')
        environment:
            NETWORK_PREFERENCE: "{\"CPU\":\"INT8,FP32\"}"
            VA_PRE: "defn(`PLATFORM')-"
            NO_PROXY: "*"
            no_proxy: "*"
')dnl

ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
    analytics:
        image: vcac-container-launcher:latest
        command: ["--network","adi_default_net","`ssai_analytics_'defn(`FRAMEWORK')_vcac-a:latest"]
        environment:
            VCAC_VA_PRE: "VCAC-A-"
            NO_PROXY: "*"
            no_proxy: "*"
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
        networks:
            - default_net 
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - node.labels.vcac_zone==yes
')dnl
