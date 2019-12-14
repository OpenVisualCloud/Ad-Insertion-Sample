
The sample can be deployed with either docker-compose (v1.20+ required) or docker swarm. The deployment uses the same configuration script.   

### Docker-Compose Deployment

This is as simple as 
```
make start_docker_compose
make stop_docker_compose
```

### Docker Swam Single Machine Deployment

Initialize docker swarm if you have not:
```
sudo docker swarm init
```
Then start/stop services as follows:
```
make start_docker_swarm
make stop_docker_swarm
```

### Docker Swam Multiple Nodes Deployment

Follow the [instructions](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm) to create a swarm. Then setup each swarm node as follows:     
- All swarm nodes must have the same user (uid) and group (gid).    
- Setup NFS to share the [volume](../../volume) directory.     
- Each swarm node must mount the [volume](../../volume) directory at the same absolute path.    

Finally, start/stop services as follows:
```
make update
make start_docker_swarm
make stop_docker_swarm
```

---

The `make update` command uploads the sample images to each worker node. If you prefer to use a private docker registry, replace with your instructions to upload the images to your docker registry.   

---

### Docker Swam Deployment with Intel VCAC-A

Initialize Intel VCAC-A if you have not:

```
script/setup-vcac-a.sh
```

Then start/stop services as follows:
```
make update
make start_docker_swarm
make stop_docker_swarm
```

### See Also:

- [Build Configuration](../../doc/cmake.md)
- [Utility Script](../../doc/script.md)

