
    kafka2db:
        image: ssai_kafka2db:latest
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

