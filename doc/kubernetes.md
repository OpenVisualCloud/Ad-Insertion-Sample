
### Setup System Environment

#### Setup Proxy

- Make sure you have required *http_proxy*, *https_proxy* and *no_proxy* setup.
```bash
export HTTP_PROXY=$http_proxy
export HTTPS_PROXY=$https_proxy
```
**Note:** This command must be run as root.

- Append this values to *no_proxy* variable. (These address are used by minikube's VM and kvm, which is integral part of Kubernetes setup. Refer [here](https://github.com/kubernetes/minikube/blob/master/docs/http_proxy.md "here"))
```bash
export no_proxy=localhost,127.0.0.1,10.96.0.0/12,192.168.99.0/24,192.168.39.0/24
export NO_PROXY=$no_proxy
```
**Note:** This command must be run as root.


#### Kubelet Proxy
You may need to setup the kubelet proxy on one machine. Below is an example to directly use the host proxy as the kubelet proxy.
```bash
mkdir -p /etc/systemd/system/kubelet.service.d/
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/kubelet.service.d/proxy.conf
```
**Note:** This command must be run as root.



### Setup Kubernetes Master Node
On this machine, run below command to setup Kubernetes master node(treat this machine as Kubernetes master node by default):
```bash
script/Kubernetes_setup_ubuntu_master.sh
```

**Note:** This script must be run as root. If there are two or more machines, please copy the Kubernetes join command from console output.

### Remove the Kubernetes environment
On all machines, run below command to remove Kubernetes:
```bash
script/Kubernetes_remove_ubuntu.sh
```
**Note:** This command must be run as root.
