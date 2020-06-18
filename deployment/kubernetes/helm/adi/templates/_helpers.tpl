{{/*
Expand the platform suffix.
*/}}
{{- define "adi.platform.suffix" -}}
{{ lower .Values.platform }}
{{- end }}

{{/*
Expand the platform volume mounts.
*/}}
{{- define "adi.platform.mounts" -}}
{{- if eq "vcac-a" ( include "adi.platform.suffix" . ) }}
            - mountPath: /var/tmp
              name: var-tmp
#          resources:
#            limits:
#              vpu.intel.com/hddl: 1
#              gpu.intel.com/i915: 1
          securityContext:
            privileged: true
{{- end }}
{{- end }}

{{/*
Expand the platform volumes.
*/}}
{{- define "adi.platform.volumes" -}}
{{- if eq "vcac-a" ( include "adi.platform.suffix" . ) }}
          - name: "var-tmp"
            hostPath:
              path: /var/tmp
              type: Directory
{{- end }}
{{- end }}

{{/*
Expand the platform nodeSelector.
*/}}
{{- define "adi.platform.node-selector" -}}
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                - key: "vcac-zone"
                  operator: NotIn
                  values:
                    - "yes"
{{- end }}

{{/*
Expand the platform accel-selector.
*/}}
{{- define "adi.platform.accel-selector" -}}
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                - key: "vcac-zone"
                  {{- if eq "vcac-a" ( include "adi.platform.suffix" . ) }}
                  operator: In
                  {{- else }}
                  operator: NotIn
                  {{- end }}
                  values:
                    - "yes"
{{- end }}

{{/*
Expand the platform device name.
*/}}
{{- define "adi.platform.device" }}
{{- if eq "vcac-a" ( include "adi.platform.suffix" . ) }}
{{- "HDDL" }}
{{- else }}
{{- "CPU" }}
{{- end }}
{{- end }}
