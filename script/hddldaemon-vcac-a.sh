#!/bin/bash -e

NODEUSER="root"
NODEIP="172.32.1.1"

# setup node to join the host docker swarm
ssh $NODEUSER@$NODEIP "source /opt/intel/openvino/bin/setupvars.sh;/opt/intel/openvino/deployment_tools/inference_engine/external/hddl/bin/hddldaemon"

