#!/usr/bin/python3

import os
import re
import subprocess
import sys
sys.path.append(sys.argv[1])

import yaml_utils

def ping(host):
    cmd = 'ping -c %d %s'%(1, host)
    p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.read().decode()

    reg_receive = "(\d+) received"
    match_receive = re.search(reg_receive, out)
    receive_count = -1

    if match_receive:
        receive_count = int(match_receive.group().split(' ')[0])
    if receive_count > 0:
        return True
    else:
        return False

#input_node_name
def input_node_name(service_name):
    if node_num == 1:
        node_name = node_name_list[0]
    else:
        node_name = input("Please input run " + service_name + " node name (" + str(node_name_list)[1:-1] + "):")
        while True:
            if node_name == "":
                node_name = node_name_list[0]
            if node_name in node_name_list:
                break
            else:
                node_name = input("Error, please input run " + service_name + " node name again (" + str(node_name_list)[1:-1] + "):")
    return node_name

node_num = int(os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p' | wc -l").read())
print("There are " + str(node_num) + " kubernetes nodes on your host server!!!")

if node_num == 0:
    os._exit(0)

node_name_list = os.popen("kubectl get node | awk '{print $1}' | sed -n '2, $p'").read().split("\n")
node_name_list = list(filter(None, node_name_list))

if node_num > 1:
    nfs_server = input("Please input where the video clips server is ([remote NFS server ip adress]):")
    while True:
        if re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",nfs_server):
            if not ping(nfs_server):
               nfs_server = input("Can't ping your NFS server ip address, Please input where the video clips server is again ([remote NFS server ip adress]):")
               continue
            adi_directory = input("Please input Ad-Insertion-Sample directory path:")
            while True:
                if not os.path.isabs(adi_directory):
                    adi_directory = input("Please input Ad-Insertion-Sample directory path:")
                else:
                    if re.match(".+/$", adi_directory):
                        adi_directory = adi_directory[:-1]
                    break
            break
        else:
            nfs_server = input("Input error, Please input where the video clips server is again ([remote NFS server ip adress]):")
else:
    nfs_server = input("Please input where the video clips server is ([localhost] or [remote NFS server ip adress]):")
    while True:
        if nfs_server == "localhost":
           adi_directory = input("Please input Ad-Insertion-Sample directory path:")
           while True:
               if not (os.path.isdir(adi_directory) and os.path.isabs(adi_directory)):
                   adi_directory = input("Please input Ad-Insertion-Sample directory path:")
               else:
                   if re.match(".+/$", adi_directory):
                       adi_directory = adi_directory[:-1]
                   break
           break
        elif re.match("((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))",nfs_server):
            if not ping(nfs_server):
               nfs_server = input("Can't ping your NFS server ip address, Please input where the video clips server is again ([localhost] or [remote NFS server ip adress]):")
               continue
            adi_directory = input("Please input Ad-Insertion-Sample directory path:")
            while True:
                if not os.path.isabs(adi_directory):
                    adi_directory = input("Please input Ad-Insertion-Sample directory path:")
                else:
                    if re.match(".+/$", adi_directory):
                        adi_directory = adi_directory[:-1]
                    break
            break
        else:
            nfs_server = input("Input error, Please input where the video clips server is again ([localhost] or [remote NFS server ip adress]):")

#zookeeper
node_name = input_node_name("zookeeper")

yaml_file = sys.argv[1] + "/zookeeper-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)

# kafka
node_name = input_node_name("kafka")

yaml_file = sys.argv[1] + "/kafka-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)

# kafka-init
node_name = input_node_name("kafka-init")

yaml_file = sys.argv[1] + "/kafka-init-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)


#database
node_name = input_node_name("database")

yaml_file = sys.argv[1] + "/database-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)

# cdn
node_name = input_node_name("cdn")

yaml_file = sys.argv[1] + "/cdn-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, "cdn")
yaml_utils.add_volumes(data, yaml_file, nfs_server, "cdn", adi_directory)

#video-analytic-ffmpeg
node_name = input_node_name("video-analytic-ffmpeg")

yaml_file = sys.argv[1] + "/video-analytic-ffmpeg-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)

#video-analytic-gstreamer
node_name = input_node_name("video-analytic-gstreamer")

yaml_file = sys.argv[1] + "/video-analytic-gstreamer-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)

#ad-transcode
node_name = input_node_name("ad-transcode")

yaml_file = sys.argv[1] + "/ad-transcode-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, "ad-transcode")
yaml_utils.add_volumes(data, yaml_file, nfs_server, "ad-transcode", adi_directory)
#yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)

#account-service
node_name = input_node_name("account-service")

yaml_file = sys.argv[1] + "/account-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
#yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)

#ad-decision
node_name = input_node_name("ad-decision")

yaml_file = sys.argv[1] + "/ad-decision-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
#yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)


#ad-content
node_name = input_node_name("ad-content")

yaml_file = sys.argv[1] + "/ad-content-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, "ad-content")
yaml_utils.add_volumes(data, yaml_file, nfs_server, "ad-content", adi_directory)

#"ad-insertion-frontend"
node_name = input_node_name("ad-insertion-frontend")

yaml_file = sys.argv[1] + "/ad-insertion-frontend-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, "ad-insertion-frontend")
yaml_utils.add_volumes(data, yaml_file, nfs_server, "ad-insertion-frontend", adi_directory)
#yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)

#analytic-db
node_name = input_node_name("analytic-db")

yaml_file = sys.argv[1] + "/analytic-db-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
#yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)

#content-provider
node_name = input_node_name("content-provider")

yaml_file = sys.argv[1] + "/content-provider-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, "content-provider")
yaml_utils.add_volumes(data, yaml_file, nfs_server, "content-provider", adi_directory)
#yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)


#content-provider-transcode
node_name = input_node_name("content-provider-transcode")

yaml_file = sys.argv[1] + "/content-provider-transcode-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, "content-provider-transcode")
yaml_utils.add_volumes(data, yaml_file, nfs_server, "content-provider-transcode", adi_directory)
#yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)

#VOLUMES NEEEDED
#ad_content
#ad-insertion-frontend
#content-provider
#content-provider-transcode
#ad-transcode

"""

node_port = 30443

yaml_file = sys.argv[1] + "/adi-service-service.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.set_nodePort(data, yaml_file, node_port)

#vod transcode
node_name = input_node_name("vod transcode")

image_name = input("Please choose the transcode mode of the vod transcode server ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
while True:
    if image_name.lower() == "sw" or  image_name.lower() == "hw":
        break
    else:
        image_name = input("Please choose the transcode mode of the vod transcode server again ([hw]: hardware is for E3/VCA2or [sw]: software is for E5):")

yaml_file = sys.argv[1] + "/vod-transcode-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_imageName(data, yaml_file, image_name.lower(), True)
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, False)
yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)

if image_name.lower() == "hw":
    node_name_list.remove(node_name)

#live_transcode
node_name = input_node_name("live transcode")

image_name = input("Please choose the transcode mode of the live transcode server ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")
while True:
    if image_name.lower() == "sw" or  image_name.lower() == "hw":
        break
    else:
        image_name = input("Please choose the transcode mode of the vod transcode server again ([hw]: hardware is for E3/VCA2 or [sw]: software is for E5):")

yaml_file = sys.argv[1] + "/live-transcode-service-deployment.yaml"
data = yaml_utils.load_yaml_file(yaml_file)
yaml_utils.update_imageName(data, yaml_file, image_name.lower(), False)
yaml_utils.update_command(data, yaml_file, image_name.lower())
yaml_utils.update_nodeSelector(data, yaml_file, node_name)
yaml_utils.add_volumeMounts(data, yaml_file, False)
yaml_utils.add_volumes(data, yaml_file, nfs_server, False, adi_directory)

"""
