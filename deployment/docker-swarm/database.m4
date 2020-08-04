
    database-service:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        environment:
            - 'discovery.type=single-node'
            - 'NO_PROXY=*'
            - 'no_proxy=*'
        networks:
            - appnet
        user: elasticsearch
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.labels.vcac_zone!=yes

