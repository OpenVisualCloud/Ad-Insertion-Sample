
version: "3.7"

secrets:
    cdn-ssl-key:
        external: true
    cdn-ssl-key:
        external: true

services:

include(common.m4)
include(analytics.defn(`PLATFORM').m4)

include(secret.m4)
ifelse(defn(`PLATFORM'),`VCAC-A',include(network.m4))

