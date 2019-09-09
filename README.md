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

### Install docker engine:        

(1) Install [docker engine](https://docs.docker.com/install).     
(2) Install [docker compose](https://docs.docker.com/compose/install), if you plan to deploy through docker compose. Version 1.20+ is required.    
(3) Setup [docker swarm](https://docs.docker.com/engine/swarm), if you plan to deploy through docker swarm. See [docker swarm setup](deployment/docker-swarm/README.md) for additional setup details.
(4) Setup [Kubernetes](https://kubernetes.io/), if you plan to deploy through Kubernetes. See [kubernetes setup](doc/kubernetes.md) for additional setup details.

### Setup docker proxy:

```bash
(4) sudo mkdir -p /etc/systemd/system/docker.service.d       
(5) printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf       
(6) sudo systemctl daemon-reload          
(7) sudo systemctl restart docker     
```

### Build docker images: 

```bash
(1) mkdir build    
(2) cd build     
(3) cmake ..    
(4) make     
```

### Generate DASH/HLS segments

By default, DASH/HLS segments are generated on the fly during playback, which requires a powerful server platform to keep up with the load. If unsure, it is recommended that you use the following commands to pre-generate DASH/HLS segments:

```bash
(5) make dash    # take a coffee break?        
(6) make hls     # take a walk?!      
```

### Start/stop services:

Use the following commands to start/stop services via docker swarm:    
```bash
(1) make start_docker_swarm      
(2) make stop_docker_swarm      
```

Use the following commands to start/stop services via docker-compose:        
```bash
(1) make start_docker_compose      
(2) make stop_docker_compose      
```
Use the following commands to start/stop services via Kubernetes:        
```bash
(1) make start_kubernetes      
(2) make stop_kubernetes      
```
**Note**: This commands must be run as root.
### Launch browser:

Launch your browser and point to `https://localhost` to play the streams and see ADs got inserted during playback. Note that if you see a browser warning of self-signed certificate, please accept it to proceed to the sample UI.    

In-case of Kubernetes, connect to `https://<system-ip>:30443`

### Customize videos:

Customize the video playlist by adding videos under [volume/video/archive](volume/video/archive) or in the build script [content-provider/archive/build.sh](content-provider/archive/build.sh).      
Rerun `make` and restart the service after making any changes.    
