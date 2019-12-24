
    database-service:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        environment:
            - 'discovery.type=single-node'
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

