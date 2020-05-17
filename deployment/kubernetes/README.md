
The Ad-Insertion sample can be deployed with Kubernetes. 

### Kubernetes Setup

1. Follow the [instructions](https://kubernetes.io/docs/setup) to setup your Kubernetes cluster.  
2. All cluster nodes must have the same user (uid) and group (gid).
3. Setup password-less access from the Kubernetes controller to each worker node (required by `make update` and `make volume`):   

```
ssh-keygen
ssh-copy-id <worker-node>
```

4. Start/stop services as follows:   

```
mkdir build
cd build
cmake ..
make
make update
make volume
make start_kubernetes
make stop_kubernetes
```

---

- The `make update` command uploads the sample images to each worker node. If you prefer to use a private docker registry, replace with your instructions to upload the images to your docker registry.   
- The `make volume` command creates local persistent volumes under the `/tmp` directory of the first two Kubernetes workers. This is a temporary solution for quick sample deployment. For scalability beyond a two-node cluster, consider rewriting the following persistent volume scripts:  
  - [**AD Archive**](ad-archive-pv.yaml.m4): Store the original AD content.   
  - [**AD Static**](ad-static-pv.yaml.m4): Store the fallback AD content.  
  - [**AD Cache**](ad-cache-pv.yaml.m4): Store the per-user transcoded DASH/HLS AD content.  
  - [**Video Archive**](video-archive-pv.yaml.m4): Store the original video content.  
  - [**Video Cache**](video-cache-pv.yaml.m4): Store the transcoded DASH/HLS video content.  

---

### See Also: 

- [Build Configuration](../../doc/cmake.md)   
- [Utility Script](../../doc/script.md)  
- [Helm Chart](helm/adi/README.md)
