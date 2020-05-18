
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
make update # optional for private registry
make start_docker_swarm
make stop_docker_swarm
```

---

The `make update` command uploads the sample images to each worker node. If you prefer to use a private docker registry, configure the sample, `cmake -DREGISTRY=<registry-url> ..`, to push the sample images to the private docker registry after each build.  

---

### Docker Swam Deployment with Intel VCAC-A

Initialize Intel VCAC-A if you have not:

```
script/setup-vcac-a.sh
```

Then start/stop services as follows:
```
make update # optional for private registry
make start_docker_swarm
make stop_docker_swarm
```

### See Also:

- [Build Configuration](../../doc/cmake.md)
- [Utility Script](../../doc/script.md)

