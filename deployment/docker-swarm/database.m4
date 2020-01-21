
    database-service:
        image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.1
        entrypoint:
            - "/bin/sh"
            - "-c"
            - "sed -ie 's/^-Xm[sx]1g//' /usr/share/elasticsearch/config/jvm.options;/usr/local/bin/docker-entrypoint.sh eswrapper"
        environment:
            - 'discovery.type=single-node'
            - 'ES_JAVA_OPTS=-Xms24g -Xmx24g'
            - 'NO_PROXY=*'
            - 'no_proxy=*'
        networks:
            - appnet
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.role==manager

