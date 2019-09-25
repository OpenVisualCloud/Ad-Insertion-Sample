    video-analytic-ffmpeg:
        image: video_analytics_service_ffmpeg:latest
        depends_on:
            - content-provider
            - kafka-service
            - zookeeper
        deploy:
            replicas: 1
        environment:
            NETWORK_PREFERENCE: "{\"CPU\":\"INT8,FP32\"}"
            VA_PRE: "Xeon-"
        restart: unless-stopped

    video-analytic-gstreamer:
        image: video_analytics_service_gstreamer:latest
        depends_on:
            - content-provider
            - kafka-service
            - zookeeper
        deploy:
            replicas: 1
        environment:
            NETWORK_PREFERENCE: "{\"CPU\":\"INT8,FP32\"}"
            VA_PRE: "Xeon-"
        restart: unless-stopped
