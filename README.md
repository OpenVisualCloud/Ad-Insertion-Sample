[![Travis Build Status](https://travis-ci.com/OpenVisualCloud/Ad-Insertion-Sample.svg?branch=master)](https://travis-ci.com/OpenVisualCloud/Ad-Insertion-Sample)
[![Stable release](https://img.shields.io/badge/latest_release-v1.0-green.svg)](https://github.com/OpenVisualCloud/Ad-Insertion-Sample/releases/tag/v1.0)
[![License](https://img.shields.io/badge/license-BSD_3_Clause-green.svg)](https://github.com/OpenVisualCloud/Ad-Insertion-Sample/blob/master/LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://github.com/OpenVisualCloud/Ad-Insertion-Sample/wiki)

The E2E sample implements a server-side AD insertion system, which features on-demand video transcoding and streaming, and AD insertion based on video content analysis.

<img src="volume/html/image/overall-arch.png" width="800">

The [Content Provider](content-provider/README.md) service serves original content, with on-demand transcoding, through the DASH or HLS streaming protocol. The [AD Insertion](ad-insertion/README.md) service analyzes video content on the fly and inserts AD, with transcoding if needed, into the video stream at each AD break slot.   

The client player is based on dash.js and hls.js.    

See additional information on each service:     
- The [Content Provider](content-provider/README.md) service     
- The [AD Insertion](ad-insertion/README.md) service
- The [AD Decision](ad-decision/README.md) service
- The [AD Content](ad-content/README.md) service
- The [Account](account/README.md) service
- The [CDN](cdn/README.md) service
- The [Video Analytics](ad-insertion/video-analytics-service/README.md) service

### Install prerequisites:

- **Timezone**: Check that the timezone setting of your host machine is correctly configured. Timezone is used during build. If you plan to run the sample on a cluster of machines managed by Docker Swarm or Kubernetes, please make sure to synchronize time among the manager/master node and worker nodes.    

- **Build Tools**: Install ```cmake``` and ```m4``` if they are not available on your system.        

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

### Build docker images: 

```bash
mkdir build    
cd build     
cmake ..    
make     
```
See also how to customize the building process with [Build Options](doc/cmake.md).

### Generate DASH/HLS segments

By default, DASH/HLS segments are generated on the fly during playback, which requires a powerful server platform to keep up with the load. If unsure, it is recommended that you use the following commands to pre-generate DASH/HLS segments:

```bash
make dash    # take a coffee break?        
make hls     # take a walk?!      
```

### Start/stop services:

Use the following commands to start/stop services via docker swarm:    
```bash
make start_docker_swarm      
make stop_docker_swarm      
```
See also how to setup [docker swarm](deployment/docker-swarm/README.md).

Use the following commands to start/stop services via docker-compose:        
```bash
make start_docker_compose      
make stop_docker_compose      
```
Use the following commands to start/stop services via Kubernetes:        
```bash
make start_kubernetes      
make stop_kubernetes      
```
**Note**: This commands must be run as root.
### Launch browser:

Launch your browser and point to `https://localhost` to play the streams and see ADs got inserted during playback. Note that if you see a browser warning of self-signed certificate, please accept it to proceed to the sample UI.    

In-case of Kubernetes, connect to `https://<system-ip>:30443`

### Customize videos:

Customize the video playlist by adding videos under [volume/video/archive](volume/video/archive) or in the build script [content-provider/archive/build.sh](content-provider/archive/build.sh).      
Rerun `make` and restart the service after making any changes.    
