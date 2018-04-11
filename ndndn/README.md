# ndndn 
♬♪   ᕕ(⌐■_■)ᕗ    ♪♬

`ndndn` (NDN Docker Net) is a set of tools and Docker images aimed at easing the process of testing NDN software as close to the real hardware as possible. 

`ndndn` utilizes [Docker Compose](https://docs.docker.com/compose/) tool - a tool for defining and running multi-container applications. For NDN developers, it allows to quickly deploy a network topology defined graphically in a `.dot` and run it using multiple Docker containers.

Running an experiment using `ndndn` is a three-step process:
* First, one prepares a `.dot` file describing experiment topology and a folder with `Dockerfile` and supporting files for the Docker image of an application being tested. 
* Then, `ndndn generate` is used to generate an experiment folder with `docker-compose.yml` configuration file which describes experiment setup in “Docker compose” terms.
* Finally, `ndndn run` is used to run the experiment.



A `.dot` file describes network topology graph a user wish to run, by defining three types of nodes (**h**ub, **p**roducer, **c**onsumer), links between these nodes and links’ properties (_latency, loss, bandwidth_). Each node of the topology graph will eventually become a Docker container when running experiment. These containers are based off of Docker images defined by `Dockerfile`s prepared during first step. There are no limits on how many containers one can run, though there is a limit (right now) on how many network-shaped links each node can have (no more than 7 right now). 

> If you are rich in hardware resources or financially, you may be interested in setting up [Docker swarm](https://docs.docker.com/engine/swarm/) in order to run very serious experiments with tens of containers. There was a time, I’ve tried swarming on Amazon EC2 instances, it was exciting.  
>   
>  ( ͡° ͜ʖ ͡°)ﾉ⌐■-■  

## build ( ´◔ ω◔`) ノシ
* macOS:

```
brew install multitail libgraphviz-dev graphviz
```

* ubuntu:

```
sudo apt-get install -y multitail libgraphviz-dev graphviz
```

* platform-independent:

```
cd ndndn
pip install pypandoc virtualenv
virtualenv env && source env/bin/activate
pip install .
```

## use  ƪ(ړײ)‎ƪ​​
* prepare app folder with `Dockerfile`  and supporting files for your application Docker image
	* see more [here]() on what  to consider when creating an app image
	* it is implied that your app can work in consumer/producer mode OR that you provide two executables in your app Docker image
* generate experiment

```
ndndn generate --topology=topology.dot --hub=`pwd`/hub --app=`pwd`/app --consumer-env=`pwd`/app/consumer.env --producer-env=`pwd`/app/producer.env
```

	* this command will generate a folder with the following:
		* `docker-compose.yml` — Docker Compose yml file describing your setup
		* `topology.pdf`
		* `hub` — symlink to the `hub` folder
		* `app` — symlink to the `app` folder
* run experiment
	* change to the newly generated folder and type:
```
ndndn run .
```

> `ndndn run` is just a wrapper around `docker-compose up -d —build` command.  
> It has not been tested against different versions of docker-compose vs docker, so if you get any errors, please report an issue or contact author.  

### collecting results

By default, docker will mount `/generated` folder from each container into a separate subfolder under `generated` folder on the host machine (like, `generated/p1`, `generated/c1`, `generated/c2` and so on). If you want to collect any results from your nodes, you should have your image configured to write to files in this directory.

## creating app image ☉ ‿ ⚆

## hub image (◕ᴥ◕ʋ)

# examples ᕕ( ᐛ )ᕗ
## ndnping (☞ﾟ∀ﾟ)☞

## ndnrtc (⌐■_■)

# describing topologies (҂◡_◡) ᕤ
