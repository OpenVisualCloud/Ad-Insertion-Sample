    video-analytic-ffmpeg:
        image: ssai_analytics_ffmpeg_xeon:latest
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

    video-analytic-gst:
        image: ssai_analytics_gst_xeon:latest
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
