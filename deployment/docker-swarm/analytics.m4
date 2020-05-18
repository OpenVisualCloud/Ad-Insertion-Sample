include(platform.m4)

    analytics:
        image: PLATFORM_IMAGE(defn(`REGISTRY_PREFIX')`ssai_analytics_'defn(`FRAMEWORK')`_'defn(`PLATFORM_SUFFIX'):latest)
        environment:
            PLATFORM_ENV(``NETWORK_PREFERENCE''): "{\"defn(`PLATFORM_DEVICE')\":\"defn(`NETWORK_PREFERENCE')\"}"
            PLATFORM_ENV(VA_PRE): "defn(`PLATFORM')-"
            PLATFORM_ENV(NO_PROXY): "*"
            PLATFORM_ENV(no_proxy): "*"
PLATFORM_ENV_EXTRA()dnl
        volumes:
            - /etc/localtime:/etc/localtime:ro
PLATFORM_VOLUME_EXTRA()dnl
        networks:
            - appnet 
        deploy:
            replicas: defn(`NANALYTICS')
            placement:
                constraints:
                    - PLATFORM_ZONE()

