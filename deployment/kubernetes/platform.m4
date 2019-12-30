define(`PLATFORM_SUFFIX',translit(defn(`PLATFORM'),`A-Z',`a-z'))dnl
define(`PLATFORM_VOLUME_MOUNTS',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
          volumeMounts:
            - mountPath: /var/tmp/hddl_service.sock
              name: var-tmp-hddl-service-sock
            - mountPath: /var/tmp/hddl_service_ready.mutex
              name: var-tmp-hddl-service-ready-mutex
            - mountPath: /var/tmp/hddl_service_alive.mutex
              name: var-tmp-hddl-service-alive-mutex
#          resources:
#            limits:
#              vpu.intel.com/hddl: 1
#              gpu.intel.com/i915: 1
           securityContext:
               privileged: true
))dnl
define(`PLATFORM_VOLUMES',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
      volumes:
          - name: var-tmp-hddl-service-sock
            hostPath:
              path: /var/tmp/hddl_service.sock
              type: Socket
          - name: var-tmp-hddl-service-ready-mutex
            hostPath:
              path: /var/tmp/hddl_service_ready.mutex
              type: File
          - name: var-tmp-hddl-service-alive-mutex
            hostPath:
              path: /var/tmp/hddl_service_alive.mutex
              type: File
))dnl
define(`PLATFORM_NODE_SELECTOR',dnl
ifelse(defn(`PLATFORM'),`VCAC-A',dnl
      nodeSelector:
          vcac-zone: "yes"
)dnl
)dnl
