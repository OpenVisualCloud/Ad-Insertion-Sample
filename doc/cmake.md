
### CMake Options:

Use the following definitions to customize the building process:   
- **REGISTRY**: Specify the URL of the private docker registry. 
- **PLATFORM**: Specify the target platform: `Xeon` or [`VCAC-A`](vcac-a.md).   
- **FRAMEWORK**: Specify the target framework: `gst` or `ffmpeg`.   
- **NANALYTICS**: Specify the number of analytics instances enabled for content analysis.  
- **NTRANSCODES**: Specify the number of transcoding instances enabled for content or AD transcoding.  
- **MINRESOLUTION**: Specify the mininum resolution to transcode for content and ad clip. `360p`, `480p`, `720p` etc.
- **NETWORK**: Specify the model network preference: `FP32`, `FP16`, `INT8` or the combination of them.  

### Examples:   

```
cd build
cmake -DPLATFORM=Xeon ..
```

```
cd build
cmake -DFRAMEWORK=ffmpeg -DPLATFORM=Xeon ..
```

### Make Commands:

- **build**: Build the sample (docker) images.  
- **update**: Distribute the sample images to worker nodes.  
- **volume**: For Kubernetes, prepare persistent volumes for the ad/content storage.  
- **dist**: Create the sample distribution package.   
- **start/stop_docker_compose**: Start/stop the sample orchestrated by docker-compose.  
- **start/stop_docker_swarm**: Start/stop the sample orchestrated by docker swarm.   
- **start/stop_kubernetes**: Start/stop the sample orchestrated by Kubernetes.   

### See Also:

- [Sample Distribution](dist.md)   
