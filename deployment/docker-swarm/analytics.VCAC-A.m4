    
    video-analytic-ffmpeg:
        image: vcac-container-launcher:latest
        command: ["--network","adi_default_net","ssai_analytics_ffmpeg_vcaca:latest"]
        depends_on:
            - content-provider
            - kafka-service
            - zookeeper
        environment:
            VCAC_VA_PRE: "VCAC-A-"
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
        networks:
            - default_net 
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.labels.vcac_zone==yes
        restart: unless-stopped

    video-analytic-gst:
        image: vcac-container-launcher:latest
        command: ["--network","adi_default_net","ssai_analytics_gst_vcaca:latest"]
        depends_on:
            - content-provider
            - kafka-service
            - zookeeper
        environment:
            VCAC_VA_PRE: "VCAC-A-"
        volumes:
            - /var/run/docker.sock:/var/run/docker.sock
        networks:
            - default_net
        deploy:
            replicas: 1
            placement:
                constraints:
                    - node.labels.vcac_zone==yes
        restart: unless-stopped
