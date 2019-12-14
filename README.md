[![Travis Build Status](https://travis-ci.com/OpenVisualCloud/Ad-Insertion-Sample.svg?branch=master)](https://travis-ci.com/OpenVisualCloud/Ad-Insertion-Sample)
[![Stable release](https://img.shields.io/badge/latest_release-v1.0-green.svg)](https://github.com/OpenVisualCloud/Ad-Insertion-Sample/releases/tag/v1.0)
[![License](https://img.shields.io/badge/license-BSD_3_Clause-green.svg)](https://github.com/OpenVisualCloud/Ad-Insertion-Sample/blob/master/LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://github.com/OpenVisualCloud/Ad-Insertion-Sample/wiki)

The E2E sample implements a server-side AD insertion system, which features on-demand video transcoding and streaming, and AD insertion based on video content analysis.

<img src="doc/overall-arch.png" width="800">

The [Content Provider](content-provider/README.md) service serves original content, with on-demand transcoding, through the DASH or HLS streaming protocol. The [AD Insertion](ad-insertion/README.md) service analyzes video content on the fly and inserts AD, with transcoding if needed, into the video stream at each AD break slot.   

### Software Stack: 

The sample exercises the following Open Visual Cloud software stacks:  

- [FFmpeg media transcoding stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/media/ffmpeg): Transcode video or Ad content to DASH or HLS, on demand.   
- [FFmpeg media analytics stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/ffmpeg): Analyze video content for objects, emotion and faces. Optimized for [Intel VCAC-A](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A/ubuntu-18.04/analytics/ffmpeg).  
- [GStreamer media analytics stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/gst): Analyze video content for objects, emotion and faces. Optimized for [Intel VCAC-A](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A/ubuntu-18.04/analytics/gst).  

### Install Prerequisites:

- **Timezone**: Check that the timezone setting of your host machine is correctly configured. Timezone is used during build. If you plan to run the sample on a cluster of machines managed by Docker Swarm or Kubernetes, please make sure to synchronize time among the manager/master node and worker nodes.    

- **Build Tools**: Install `cmake` and `m4` if they are not available on your system.        

- **Docker Engine**:        
  - Install [docker engine](https://docs.docker.com/install).     
  - Install [docker compose](https://docs.docker.com/compose/install), if you plan to deploy through docker compose. Version 1.20+ is required.    
  - Setup [docker swarm](https://docs.docker.com/engine/swarm), if you plan to deploy through docker swarm. See [Docker Swarm Setup](deployment/docker-swarm/README.md) for additional setup details.  
  - Setup [Kubernetes](https://kubernetes.io/docs/setup), if you plan to deploy through Kubernetes. See [Kubernetes Setup](deployment/kubernetes/README.md) for additional setup details.     
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
See also how to customize the building process with [Build Options](doc/cmake.md).

### Generate DASH/HLS

By default, DASH/HLS segments are generated on the fly during playback, which requires a powerful server platform to keep up with the load. If unsure, it is recommended that you use the following commands to pre-generate DASH/HLS segments:

```bash
make dash    # take a coffee break?        
make hls     # take a walk?!      
```

### Start/stop Services:

Use the following commands to start/stop services via docker swarm (see also [Docker Swarm Setup](deployment/docker-swarm/README.md)).    

```bash
make update
make start_docker_swarm      
make stop_docker_swarm      
```

Use the following commands to start/stop services via docker-compose:        

```bash
make start_docker_compose      
make stop_docker_compose      
```

Use the following commands to start/stop services via Kubernetes (see also [Kubernetes Setup](deployment/kubernetes/README.md)):        

```bash
make update
make volume
make start_kubernetes      
make stop_kubernetes      
```

### Launch browser:

Launch your browser and point to `https://<hostname>` to play the streams and see ADs got inserted during playback. 

---

- For Kubernetes/Docker Swarm, `<hostname>` is the hostname of the manager/master node.
- If you see a browser warning of self-signed certificate, please accept it to proceed to the sample UI.

---

### See Also:

- [The Content Provider Service](content-provider/README.md)  
- [The AD Insertion Service](ad-insertion/README.md)  
- [The AD Decision Service](ad-content/ad-decision/README.md)  
- [The AD Content Service](ad-content/README.md)  
- [The Account Service](account/README.md) 
- [The CDN Service](cdn/README.md) 
- [The Analytics Service](ad-insertion/analytics/README.md) 
- [Docker Swarm Setup](deployment/docker-swarm/README.md)  
- [Kubernetes Setup](deployment/kubernetes/README.md)  
- [Build Confiugration](doc/cmake.md)   
- [Customize Videos](doc/customize.md)   
- [Sample Distribution](doc/dist.md)  
- [Utility Script](doc/script.md)  
