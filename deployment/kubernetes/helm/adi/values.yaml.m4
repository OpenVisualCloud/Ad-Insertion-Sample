
# private registry URL
registryPrefix: ""

# platform specifies the target platform: Xeon or VCAC-A.
platform: "defn(`PLATFORM')"

# framework specifies the target framework: gst or ffmpeg.
framework: "defn(`FRAMEWORK')"

# nanalytics specifies the number of analytics instances
nanalytics: defn(`NANALYTICS')

# ntranscodes specifies the number of transcoding instances
ntranscodes: defn(`NTRANSCODES')

# hostIP specifies the external IP to access the sample UI
hostIP: "defn(`HOSTIP')"

# network specifies the analytics model precision: FP32, INT8 or FP16, or their 
# combination as a comma delimited string. 
networkPreference: "defn(`NETWORK_PREFERENCE')"

# pvc specifies the persistent volume claim sizes
pvc:
  ad:
    archive: defn(`AD_ARCHIVE_VOLUME_SIZE')Gi
    cache: defn(`AD_CACHE_VOLUME_SIZE')Gi
    segment: defn(`AD_SEGMENT_VOLUME_SIZE')Gi
    static: defn(`AD_STATIC_VOLUME_SIZE')Gi
  video:
    archive: defn(`VIDEO_ARCHIVE_VOLUME_SIZE')Gi
    cache: defn(`VIDEO_CACHE_VOLUME_SIZE')Gi

# optional: provide Linux user id & group permissioned to access cloud storage
# userID is obtained using command: `$ id -u`
# groupID is obtained using command: `$ id -g`
userId: defn(`USERID')
groupId: defn(`GROUPID')
