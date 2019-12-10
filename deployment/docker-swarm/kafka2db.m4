
    kafka2db:
        image: ssai_kafka2db:latest
        depends_on:
            - kafka-service
            - database
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

