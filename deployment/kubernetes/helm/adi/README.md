
The AD-Insertion sample implements a server-side AD insertion system, which features on-demand video transcoding and streaming, and AD insertion based on video content analysis.

### Software Stack: 

The sample is powered by the following Open Visual Cloud software stacks:  

- The [FFmpeg-based media transcoding software stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/media/ffmpeg) is used to transcode video or Ad content to DASH or HLS during playback. The software stack is optimized for [Intel® Xeon® Scalable Processors](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/media/ffmpeg).     
- The [FFmpeg-based media analytics software stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/ffmpeg) is used, with `FRAMEWORK=ffmpeg`, to analyze video content for objects, emotion and faces during playback. The software stack is optimized for [Intel Xeon Scalable Processors](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/ffmpeg) and [Intel VCAC-A](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A/ubuntu-18.04/analytics/ffmpeg).  
- The [GStreamer-based media analytics software stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/gst) is used, with `FRAMEWORK=gst`, to analyze video content for objects, emotion and faces during playback. The software stack is optimized for [Intel Xeon Scalable Processors](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/gst) and [Intel VCAC-A](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A/ubuntu-18.04/analytics/gst).  

### Install Prerequisites:

- **Timezone**: Check that the timezone setting of your host machine is correctly configured. Timezone is used during build. If you plan to run the sample on a cluster of machines managed by Docker Swarm or Kubernetes, please make sure to synchronize time among the manager/master node and worker nodes.    

- **Build Tools**: Install `cmake` and `m4` if they are not available on your system.        

- **Docker Engine**:        
  - Install [docker engine](https://docs.docker.com/install). Make sure you [setup](https://docs.docker.com/install/linux/linux-postinstall) docker to run as a regular user.       
  - Setup [Kubernetes](https://kubernetes.io/docs/setup) and [helm](https://helm.sh/docs/intro/install).  
  - Setup docker proxy as follows if you are behind a firewall:   

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d       
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf       
sudo systemctl daemon-reload          
sudo systemctl restart docker     
```

### Build: 

```bash
mkdir build    
cd build     
cmake ..    
make     
```

### Generate DASH/HLS

By default, DASH/HLS segments are generated on the fly during playback, which requires a powerful server platform to keep up with the load. If unsure, it is recommended that you use the following commands to pre-generate DASH/HLS segments:

```bash
#content segment
make dash    # take a coffee break?        
make hls     # take a walk?!      

# ad segment
make addash
make adhls
```

### Start/stop Services:

Use the following commands to start/stop services via Kubernetes:

```bash
make update # optional for private registry
make volume
make start_helm     
make stop_helm
```

---

- The `make update` command uploads the sample images to each worker node. If you prefer to use a private docker registry, configure the sample, `cmake -DREGISTRY=<registry-url> ..`, to push the sample images to the private registry after each build.
- The `make volume` command creates local persistent volumes under the `/tmp` directory of the first two Kubernetes workers. This is a temporary solution for quick sample deployment. For scalability beyond a two-node cluster, consider rewriting the persistent volume scripts.

---

### Launch browser:

Launch your browser and point to `https://<hostname>` to play the streams and see ADs got inserted during playback. 

---

- For Kubernetes/Docker Swarm, `<hostname>` is the hostname of the manager/master node.
- If you see a browser warning of self-signed certificate, please accept it to proceed to the sample UI.

---

