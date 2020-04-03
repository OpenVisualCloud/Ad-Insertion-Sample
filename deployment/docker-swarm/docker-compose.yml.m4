
version: "3.7"

secrets:
    cdn-ssl-key:
        external: true
    cdn-ssl-key:
        external: true

services:

include(zookeeper.m4)
include(kafka.m4)
include(database.m4)
include(account.m4)
include(ad-decision.m4)
include(ad-content.m4)
include(ad-insertion.m4)
include(kafka2db.m4)
include(cdn.m4)
include(content-provider.m4)
include(content-transcode.m4)
include(ad-transcode.m4)
include(analytics.m4)
include(ad-workload.m4)
include(secret.m4)
include(network.m4)
