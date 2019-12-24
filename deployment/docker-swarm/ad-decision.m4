
    ad-decision-service:
        image: ssai_ad_decision_frontend:latest
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

