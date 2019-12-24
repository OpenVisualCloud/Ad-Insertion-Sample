
    account-service:
        image: ssai_account_service:latest
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

