
The Ad-Insertion sample can be deployed with Kubernetes. 

### Kubernetes Setup

1. Follow the [instructions](https://kubernetes.io/docs/setup) to setup your Kubernetes cluster.  

2. Setup password-less access from the Kubernetes controller to each worker node (required by ```make update```):   

```
ssh-keygen
ssh-copy-id <worker-node>
```

3. Start/stop services as follows:   

```
mkdir build
cd build
cmake ..
make
make update
make start_kubernetes
make stop_kubernetes
```

---

The command ```make update``` uploads the sample images to each worker node. If you prefer to use a private docker registry, replace with your instructions to upload the images to your docker registry.   

---

