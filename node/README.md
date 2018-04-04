# NDN Docker Image

## Build Image

```
docker build -t hub .
```

### Build specific release

Pass `VERSION_CXX` and `VERSION_NFD` arguments at build stage:

```
docker build -t hub-0.6.1 --build-arg VERSION_CXX=ndn-cxx-0.6.1 --build-arg VERSION_NFD=NFD-0.6.1 .
```

## Run Image

### Start as default container

```
docker run -d --rm --name hub1 hub
```

Query status:

```
docker exec hub1 nfd --version
docker exec hub1 nfd-status
```

### Start container with ports exposing:

```
docker run -d --rm --name hub1 -p 6364:6363 -p 6365:6363/udp hub
``` 

> If you want to run NFD as a service inside of container to accept outside connections, map TCP and UDP ports to 6363:
> ```
> docker run -d --rm --name hub1 -p 6363:6363 -p 6363:6363/udp hub
> ```

### Creating faces

You can create faces from your local machine towards conatiner (this will only work if container was started with ports exposing, as described above):

```
nfdc face create tcp://localhost:6364
nfdc face create tcp://localhost:6365
```

Or vice versa:

```
docker exec hub1 nfdc face create udp://<ip-address>
```

### Custom config file

To start NDN container with custom config file, copy your config file to designated folder and mount it into the container:

```
mkdir conf
cp <path-to-config>/nfd.conf conf/
docker run -d --rm --name hub1 -v $(pwd)/conf:/cong -e CONFIG=/conf/nfd.conf hub
```

### Saving log to host machine

To save log file to a host machine, mount logs folder into a designated folder on a host machine:

```
mkdir logs
docker run -d --rm --name hub1 -v $(pwd)/logs:/logs hub
```

> To start container with custom config *and* saving log to a host machine, combine commands above:
> ```
> mkdir conf logs
> cp <path-to-config>/nfd.conf conf/
> docker run -d --rm --name hub1 -p 6364:6363 -p 6365:6363/udp -v $(pwd)/logs:/logs -v $(pwd)/conf:/conf -e CONFIG=/conf/nfd.conf hub
> ```