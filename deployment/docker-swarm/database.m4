
    database:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.6.0
        environment:
            - 'discovery.type=single-node'
            - 'ES_JAVA_OPTS=-Xms1024m -Xmx1024m'
        ulimits:
            memlock:
                soft: -1
                hard: -1
        restart: always
ifelse(defn(`PLATFORM'),`VCAC-A',`dnl
        networks:
            - default_net
')dnl
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

