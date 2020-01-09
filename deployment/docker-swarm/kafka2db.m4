
    kafka2db:
        image: ssai_kafka2db:latest
        environment:
            INGEST_DURATION: "0.1"
            INGEST_BATCH: "50"
            NO_PROXY: "*"
            no_proxy: "*"
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

